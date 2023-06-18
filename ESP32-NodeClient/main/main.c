/* main.c - Application main entry point */

/*
 * Copyright (c) 2017 Intel Corporation
 * Additional Copyright (c) 2018 Espressif Systems (Shanghai) PTE LTD
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "esp_log.h"
#include "nvs_flash.h"

#include "esp_ble_mesh_common_api.h"
#include "esp_ble_mesh_provisioning_api.h"
#include "esp_ble_mesh_networking_api.h"
#include "esp_ble_mesh_config_model_api.h"
#include "esp_ble_mesh_generic_model_api.h"

#include "board.h"
#include "ble_mesh_example_init.h"
#include "ble_mesh_example_nvs.h"

#include <stdint.h>
#include <stddef.h>
#include "esp_wifi.h"
#include "esp_system.h"
#include "esp_event.h"
#include "esp_netif.h"
#include "protocol_examples_common.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
#include "freertos/queue.h"

#include "lwip/sockets.h"
#include "lwip/dns.h"
#include "lwip/netdb.h"
#include "mqtt_client.h"

#include "esp_timer.h"
#include <esp_bt.h>

#define TRUE 0x01
#define FALSE 0x00

#define  EXAMPLE_ESP_WIFI_SSID ""
#define  EXAMPLE_ESP_WIFI_PASS ""
#define MAX_RETRY 10
#define TAG "EXAMPLE"
#define CID_ESP 0x02E5

static const char *TAG_MQTT = "MQTT";
static int retry_cnt = 0;
static void mqtt_app_start(void);

esp_mqtt_client_handle_t client = NULL;

uint32_t MQTT_CONNEECTED = 0;
uint32_t autoincrement_value = 0;
uint32_t defaultTTLValue = 4;

static uint8_t dev_uuid[16] = { 0xdd, 0xdd };
uint64_t timer;
static struct example_info_store {
    uint16_t net_idx;   /* NetKey Index */
    uint16_t app_idx;   /* AppKey Index */
    uint8_t  onoff;     /* Remote OnOff */
    uint8_t tid;       /* Message TID */
    uint8_t trans_time;
} __attribute__((packed)) store = {
    .net_idx = ESP_BLE_MESH_KEY_UNUSED,
    .app_idx = ESP_BLE_MESH_KEY_UNUSED,
    .onoff = 0x0,
    .tid = 0x0,
    .trans_time = 0x0,
};

int idWithSendTime[64];
int currentlIdWithSendTime = 0;

int PDRSend = 0;
int PDRReceived = 0;
uint8_t Start = FALSE;



static nvs_handle_t NVS_HANDLE;
static const char * NVS_KEY = "onoff_client";

static esp_ble_mesh_client_t onoff_client;

esp_ble_mesh_cfg_srv_t config_server = {
    .relay = ESP_BLE_MESH_RELAY_DISABLED,
    .beacon = ESP_BLE_MESH_BEACON_ENABLED,
#if defined(CONFIG_BLE_MESH_FRIEND)
    .friend_state = ESP_BLE_MESH_FRIEND_ENABLED,
#else
    .friend_state = ESP_BLE_MESH_FRIEND_NOT_SUPPORTED,
#endif
#if defined(CONFIG_BLE_MESH_GATT_PROXY_SERVER)
    .gatt_proxy = ESP_BLE_MESH_GATT_PROXY_ENABLED,
#else
    .gatt_proxy = ESP_BLE_MESH_GATT_PROXY_NOT_SUPPORTED,
#endif
    .default_ttl = 4,
    /* 3 transmissions with 20ms interval */
    .net_transmit = ESP_BLE_MESH_TRANSMIT(2, 20),
    .relay_retransmit = ESP_BLE_MESH_TRANSMIT(2, 20),
};

uint16_t TN = 2;
uint16_t TI = 20;

ESP_BLE_MESH_MODEL_PUB_DEFINE(onoff_cli_pub, 2 + 1, ROLE_NODE);

static esp_ble_mesh_model_t root_models[] = {
    ESP_BLE_MESH_MODEL_CFG_SRV(&config_server),
    ESP_BLE_MESH_MODEL_GEN_ONOFF_CLI(&onoff_cli_pub, &onoff_client),
};

static esp_ble_mesh_elem_t elements[] = {
    ESP_BLE_MESH_ELEMENT(0, root_models, ESP_BLE_MESH_MODEL_NONE),
};

static esp_ble_mesh_comp_t composition = {
    .cid = CID_ESP,
    .elements = elements,
    .element_count = ARRAY_SIZE(elements),
};

/* Disable OOB security for SILabs Android app */
static esp_ble_mesh_prov_t provision = {
    .uuid = dev_uuid,
#if 0
    .output_size = 4,
    .output_actions = ESP_BLE_MESH_DISPLAY_NUMBER,
    .input_actions = ESP_BLE_MESH_PUSH,
    .input_size = 4,
#else
    .output_size = 0,
    .output_actions = 0,
#endif
};

static void mesh_example_info_store(void)
{
    ble_mesh_nvs_store(NVS_HANDLE, NVS_KEY, &store, sizeof(store));
}

static void mesh_example_info_restore(void)
{
    esp_err_t err = ESP_OK;
    bool exist = false;

    err = ble_mesh_nvs_restore(NVS_HANDLE, NVS_KEY, &store, sizeof(store), &exist);
    if (err != ESP_OK) {
        return;
    }

    if (exist) {
        ESP_LOGI(TAG, "Restore, net_idx 0x%04x, app_idx 0x%04x, onoff %u, tid 0x%02x",
            store.net_idx, store.app_idx, store.onoff, store.tid);
    }
}

static void prov_complete(uint16_t net_idx, uint16_t addr, uint8_t flags, uint32_t iv_index)
{
    ESP_LOGI(TAG, "net_idx: 0x%04x, addr: 0x%04x", net_idx, addr);
    ESP_LOGI(TAG, "flags: 0x%02x, iv_index: 0x%08x", flags, iv_index);
    board_led_operation(LED_G, LED_OFF);
    store.net_idx = net_idx;
    /* mesh_example_info_store() shall not be invoked here, because if the device
     * is restarted and goes into a provisioned state, then the following events
     * will come:
     * 1st: ESP_BLE_MESH_NODE_PROV_COMPLETE_EVT
     * 2nd: ESP_BLE_MESH_PROV_REGISTER_COMP_EVT
     * So the store.net_idx will be updated here, and if we store the mesh example
     * info here, the wrong app_idx (initialized with 0xFFFF) will be stored in nvs
     * just before restoring it.
     */
}

static void example_ble_mesh_provisioning_cb(esp_ble_mesh_prov_cb_event_t event,
                                             esp_ble_mesh_prov_cb_param_t *param)
{
    switch (event) {
    case ESP_BLE_MESH_PROV_REGISTER_COMP_EVT:
        ESP_LOGI(TAG, "ESP_BLE_MESH_PROV_REGISTER_COMP_EVT, err_code %d", param->prov_register_comp.err_code);
        mesh_example_info_restore(); /* Restore proper mesh example info */
        break;
    case ESP_BLE_MESH_NODE_PROV_ENABLE_COMP_EVT:
        ESP_LOGI(TAG, "ESP_BLE_MESH_NODE_PROV_ENABLE_COMP_EVT, err_code %d", param->node_prov_enable_comp.err_code);
        break;
    case ESP_BLE_MESH_NODE_PROV_LINK_OPEN_EVT:
        ESP_LOGI(TAG, "ESP_BLE_MESH_NODE_PROV_LINK_OPEN_EVT, bearer %s",
            param->node_prov_link_open.bearer == ESP_BLE_MESH_PROV_ADV ? "PB-ADV" : "PB-GATT");
        break;
    case ESP_BLE_MESH_NODE_PROV_LINK_CLOSE_EVT:
        ESP_LOGI(TAG, "ESP_BLE_MESH_NODE_PROV_LINK_CLOSE_EVT, bearer %s",
            param->node_prov_link_close.bearer == ESP_BLE_MESH_PROV_ADV ? "PB-ADV" : "PB-GATT");
        break;
    case ESP_BLE_MESH_NODE_PROV_COMPLETE_EVT:
        ESP_LOGI(TAG, "ESP_BLE_MESH_NODE_PROV_COMPLETE_EVT");
        prov_complete(param->node_prov_complete.net_idx, param->node_prov_complete.addr,
            param->node_prov_complete.flags, param->node_prov_complete.iv_index);
        break;
    case ESP_BLE_MESH_NODE_PROV_RESET_EVT:
        break;
    case ESP_BLE_MESH_NODE_SET_UNPROV_DEV_NAME_COMP_EVT:
        ESP_LOGI(TAG, "ESP_BLE_MESH_NODE_SET_UNPROV_DEV_NAME_COMP_EVT, err_code %d", param->node_set_unprov_dev_name_comp.err_code);
        break;
    default:
        break;
    }
}

void example_ble_mesh_send_gen_onoff_set(void)
{
    
    esp_ble_mesh_generic_client_set_state_t set = {0};
    esp_ble_mesh_client_common_param_t common = {0};
    esp_err_t err = ESP_OK;

    common.opcode = ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_SET_UNACK;
    common.model = onoff_client.model;
    common.ctx.net_idx = store.net_idx;
    common.ctx.app_idx = store.app_idx;
    common.ctx.addr = 0xFFFF;   /* to all nodes */
    common.ctx.send_ttl = 3;
    common.ctx.send_rel = false;
    common.msg_timeout = 0;     /* 0 indicates that timeout value from menuconfig will be used */
    common.msg_role = ROLE_NODE;

    set.onoff_set.op_en = true;
    set.onoff_set.onoff = store.onoff;
    set.onoff_set.tid = store.tid++;
    
    timer = esp_timer_get_time();
    //ESP_LOGI("PACKET_RECEIVED", "%llu", timer);
    err = esp_ble_mesh_generic_client_set_state(&common, &set);
    if (err) {
        ESP_LOGE(TAG, "Send Generic OnOff Set Unack failed");
        return;
    }
    store.onoff = !store.onoff;
    mesh_example_info_store(); /* Store proper mesh example info */
    
}

void example_ble_mesh_send_gen_onoff_set2(void)
{
    esp_ble_mesh_generic_client_set_state_t set = {0};
    esp_ble_mesh_client_common_param_t common = {0};
    esp_err_t err = ESP_OK;

    common.opcode = ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_SET_UNACK;
    common.model = onoff_client.model;
    common.ctx.net_idx = store.net_idx;
    common.ctx.app_idx = store.app_idx;
    common.ctx.addr = 0xFFFF;   /* to all nodes */
    common.ctx.send_ttl = defaultTTLValue;
    common.ctx.send_rel = true;
    common.msg_timeout = 0;     /* 0 indicates that timeout value from menuconfig will be used */
    common.msg_role = ROLE_NODE;

    uint8_t identificatoreMsg = 0;   
    uint8_t MessaggioID = currentlIdWithSendTime;
    // uint8_t MessaggioID = 0;
    uint8_t combinazione = 0;
    combinazione |= (identificatoreMsg << 6);
    combinazione |= MessaggioID;
    // printf("Combinazione: %u\n", combinazione); 

    set.onoff_set.op_en = false;
    set.onoff_set.onoff = combinazione;
    set.onoff_set.tid = autoincrement_value++;
    set.onoff_set.trans_time = 0x003;

    timer = esp_timer_get_time();
    idWithSendTime[currentlIdWithSendTime] = timer;
    currentlIdWithSendTime = currentlIdWithSendTime + 1;

    if (currentlIdWithSendTime>15) {
        currentlIdWithSendTime = 0;
        vTaskDelay(10000 / portTICK_PERIOD_MS);
    }

    err = esp_ble_mesh_generic_client_set_state(&common, &set);
    if (err) {
        ESP_LOGE(TAG, "Send Generic OnOff Set Unack failed");
        return;
    } else {
        PDRSend = PDRSend + 1;
    }
    store.onoff = !store.onoff;
    mesh_example_info_store(); /* Store proper mesh example info */
}

void SendNewParameterValue(uint8_t parametro, uint8_t valore, char address[10])
{
    esp_ble_mesh_generic_client_set_state_t set = {0};
    esp_ble_mesh_client_common_param_t common = {0};
    esp_err_t err = ESP_OK;

    ESP_LOGI(TAG, "parametro %d", parametro);
    ESP_LOGI(TAG, "valore %d", valore);
    ESP_LOGI(TAG, "address %s", address);
    
    common.opcode = ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_SET_UNACK;
    common.model = onoff_client.model;
    common.ctx.net_idx = store.net_idx;
    common.ctx.app_idx = store.app_idx;
    common.ctx.addr = 0xFFFF;   /* to all nodes */
    common.ctx.send_ttl = 7;
    common.ctx.send_rel = true;
    common.msg_timeout = 0;     /* 0 indicates that timeout value from menuconfig will be used */
    common.msg_role = ROLE_NODE;
    
    uint8_t identificatore = 1;
    uint8_t combinazione = ((identificatore & 0x01) << 7) | ((parametro & 0x03) << 5) | (valore & 0x1F);
    ESP_LOGI(TAG, "combinazione 0x%x", combinazione);

    set.onoff_set.op_en = false;
    set.onoff_set.onoff = combinazione;
    set.onoff_set.tid = autoincrement_value++;
    set.onoff_set.trans_time = 0x003;

    timer = esp_timer_get_time();
    err = esp_ble_mesh_generic_client_set_state(&common, &set);
    if (err) {
        ESP_LOGE(TAG, "Send Generic OnOff Set Unack failed");
        return;
    }
}

static void example_ble_mesh_generic_client_cb(esp_ble_mesh_generic_client_cb_event_t event,
                                               esp_ble_mesh_generic_client_cb_param_t *param)
{
    ESP_LOGI("BLE MESH----", "opcode is 0x%04x",  param->status_cb.onoff_status.present_onoff); // ID del messaggio 
    switch (event) {
        case ESP_BLE_MESH_GENERIC_CLIENT_GET_STATE_EVT:
            ESP_LOGI(TAG, "ESP_BLE_MESH_GENERIC_CLIENT_GET_STATE_EVT");
            if (param->params->opcode == ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_GET) {
                ESP_LOGI(TAG, "ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_GET, onoff %d", param->status_cb.onoff_status.present_onoff);
            }
            break;
        case ESP_BLE_MESH_GENERIC_CLIENT_SET_STATE_EVT:
            ESP_LOGI(TAG, "ESP_BLE_MESH_GENERIC_CLIENT_SET_STATE_EVT");
            if (param->params->opcode == ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_SET) {
                ESP_LOGI(TAG, "ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_SET, onoff %d", param->status_cb.onoff_status.present_onoff);
            }
            break;
        case ESP_BLE_MESH_GENERIC_CLIENT_PUBLISH_EVT:
            PDRReceived = PDRReceived + 1;
            int returnTime = esp_timer_get_time();
            uint8_t messageReturn = param->status_cb.onoff_status.present_onoff;

            uint8_t nodeID = (messageReturn >> 6) & 0x03;       // i primi due bit di combinazione spostati a destra di 6 posizioni
            uint8_t TTLResidue = (messageReturn >> 4) & 0x03;   // i successivi due bit di combinazione spostati a destra di 4 posizioni e poi mascherati con 0x03
            uint8_t messageID = messageReturn & 0x0F;           // gli ultimi 4 bit di combinazione mascherati con 0x0F

            ESP_LOGI("BLE MESH", "Messaggio ricevuto %d", messageReturn);
            ESP_LOGI("BLE MESH", "Node Id%d", nodeID);
            ESP_LOGI("BLE MESH", "TTL residue %d", TTLResidue);
            ESP_LOGI("BLE MESH", "messageID %d", messageID);
            ESP_LOGI("BLE MESH", "------------- returnTime %d", returnTime);
            ESP_LOGI("BLE MESH", "------------- idWithSendTime[messageID] %d", idWithSendTime[messageID]);
            int totalTime = returnTime - idWithSendTime[messageID];
            ESP_LOGI("BLE MESH", "totalTime %d",  totalTime);
        
            char Performances[30];
            sprintf(Performances, "%d-%d-%d", nodeID, TTLResidue, totalTime);  // Formattiamo la stringa con i tre valori uint8_t separati da trattini
            printf("Performances formattata è: %s\n", Performances);

            if(MQTT_CONNEECTED) {
                esp_mqtt_client_publish(client, "/sendPerformnce",  Performances, 0, 0, 0);
            }
            break;
        case ESP_BLE_MESH_GENERIC_CLIENT_TIMEOUT_EVT:
            printf("SONO QUI 5");
            ESP_LOGI(TAG, "ESP_BLE_MESH_GENERIC_CLIENT_TIMEOUT_EVT");
            if (param->params->opcode == ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_SET) {
                /* If failed to get the response of Generic OnOff Set, resend Generic OnOff Set  */
                example_ble_mesh_send_gen_onoff_set();
            }
            break;
        default:
            break;
    }
}

static void example_ble_mesh_config_server_cb(esp_ble_mesh_cfg_server_cb_event_t event,
                                              esp_ble_mesh_cfg_server_cb_param_t *param)
{
    if (event == ESP_BLE_MESH_CFG_SERVER_STATE_CHANGE_EVT) {
        switch (param->ctx.recv_op) {
        case ESP_BLE_MESH_MODEL_OP_APP_KEY_ADD:
            ESP_LOGI(TAG, "ESP_BLE_MESH_MODEL_OP_APP_KEY_ADD");
            ESP_LOGI(TAG, "net_idx 0x%04x, app_idx 0x%04x",
                param->value.state_change.appkey_add.net_idx,
                param->value.state_change.appkey_add.app_idx);
            ESP_LOG_BUFFER_HEX("AppKey", param->value.state_change.appkey_add.app_key, 16);
            break;
        case ESP_BLE_MESH_MODEL_OP_MODEL_APP_BIND:
            ESP_LOGI(TAG, "ESP_BLE_MESH_MODEL_OP_MODEL_APP_BIND");
            ESP_LOGI(TAG, "elem_addr 0x%04x, app_idx 0x%04x, cid 0x%04x, mod_id 0x%04x",
                param->value.state_change.mod_app_bind.element_addr,
                param->value.state_change.mod_app_bind.app_idx,
                param->value.state_change.mod_app_bind.company_id,
                param->value.state_change.mod_app_bind.model_id);
            if (param->value.state_change.mod_app_bind.company_id == 0xFFFF &&
                param->value.state_change.mod_app_bind.model_id == ESP_BLE_MESH_MODEL_ID_GEN_ONOFF_CLI) {
                store.app_idx = param->value.state_change.mod_app_bind.app_idx;
                mesh_example_info_store(); /* Store proper mesh example info */
            }
            break;
        default:
            break;
        }
    }
}

static esp_err_t ble_mesh_init(void)
{
    esp_err_t err = ESP_OK;

    esp_ble_mesh_register_prov_callback(example_ble_mesh_provisioning_cb);
    esp_ble_mesh_register_generic_client_callback(example_ble_mesh_generic_client_cb);
    esp_ble_mesh_register_config_server_callback(example_ble_mesh_config_server_cb);

    err = esp_ble_mesh_init(&provision, &composition);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to initialize mesh stack (err %d)", err);
        return err;
    }

    err = esp_ble_mesh_node_prov_enable(ESP_BLE_MESH_PROV_ADV | ESP_BLE_MESH_PROV_GATT);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to enable mesh node (err %d)", err);
        return err;
    }

    ESP_LOGI(TAG, "BLE Mesh Node initialized");
    board_led_operation(LED_G, LED_ON);

    return err;
}

static esp_err_t wifi_event_handler(void *arg, esp_event_base_t event_base,
                                   int32_t event_id, void *event_data)
{
    switch (event_id)
    {
    case WIFI_EVENT_STA_START:
        esp_wifi_connect();
        ESP_LOGI(TAG_MQTT, "Trying to connect with Wi-Fi\n");
        break;

    case WIFI_EVENT_STA_CONNECTED:
        ESP_LOGI(TAG_MQTT, "Wi-Fi connected\n");
        break;

    case IP_EVENT_STA_GOT_IP:
        ESP_LOGI(TAG_MQTT, "got ip: startibg MQTT Client\n");
        mqtt_app_start();
        break;

    case WIFI_EVENT_STA_DISCONNECTED:
        ESP_LOGI(TAG_MQTT, "disconnected: Retrying Wi-Fi\n");
        if (retry_cnt++ < MAX_RETRY)
        {
            esp_wifi_connect();
        }
        else
        ESP_LOGI(TAG_MQTT, "Max Retry Failed: Wi-Fi Connection\n");
        break;

    default:
        break;
    }
    return ESP_OK;
}

void wifi_init(void)
{
    esp_event_loop_create_default();
    esp_event_handler_register(WIFI_EVENT, ESP_EVENT_ANY_ID, &wifi_event_handler, NULL);
    esp_event_handler_register(IP_EVENT, IP_EVENT_STA_GOT_IP, &wifi_event_handler, NULL);

    wifi_config_t wifi_config = {
        .sta = {
            .ssid = EXAMPLE_ESP_WIFI_SSID,
            .password = EXAMPLE_ESP_WIFI_PASS,
	     .threshold.authmode = WIFI_AUTH_WPA2_PSK,
        },
    };
    esp_netif_init();
    esp_netif_create_default_wifi_sta();
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    esp_wifi_init(&cfg);
    esp_wifi_set_mode(WIFI_MODE_STA);
    esp_wifi_set_config(ESP_IF_WIFI_STA, &wifi_config);
    esp_wifi_start();
}

void off_all_LED(){
    board_led_operation(LED_G, LED_OFF);
    board_led_operation(LED_R, LED_OFF);
    board_led_operation(LED_B, LED_OFF);
}

/*
 * @brief Event handler registered to receive MQTT events
 *
 *  This function is called by the MQTT client event loop.
 *
 * @param handler_args user data registered to the event.
 * @param base Event base for the handler(always MQTT Base in this example).
 * @param event_id The id for the received event.
 * @param event_data The data for the event, esp_mqtt_event_handle_t.
 */


esp_err_t set_tx_power(esp_power_level_t power_level) {
    printf('sono dentro a set_tx_power');
    esp_err_t ret;
    ret = esp_ble_tx_power_set(ESP_BLE_PWR_TYPE_CONN_HDL0, power_level);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to set BLE connection power, error code = %x", ret);
        board_led_operation(LED_R, LED_ON);
    } else {
        ESP_LOGI(TAG, "BLE connection power set to %d dBm", power_level);
    }
    return ret;
}

void splitString(char* str, char** result) {
    int i = 0;
    char* token = strtok(str, ":");

    while (token != NULL) {
        result[i] = token;
        token = strtok(NULL, ":");
        i++;
    }
}

static void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data)
{
    ESP_LOGD(TAG_MQTT, "Event dispatched from event loop base=%s, event_id=%d", base, event_id);
    esp_mqtt_event_handle_t event = event_data;
    esp_mqtt_client_handle_t client = event->client;
    int msg_id;
    char* result[2];

    switch ((esp_mqtt_event_id_t)event_id)
    {
    case MQTT_EVENT_CONNECTED:
        ESP_LOGI(TAG_MQTT, "MQTT_EVENT_CONNECTED");
        MQTT_CONNEECTED=1;
        
        msg_id = esp_mqtt_client_subscribe(client, "/setTRA", 1);
        ESP_LOGI(TAG_MQTT, "sent subscribe successful, msg_id=%d", msg_id);

        msg_id = esp_mqtt_client_subscribe(client, "/setPower", 0);
        ESP_LOGI(TAG_MQTT, "sent subscribe successful, msg_id=%d", msg_id);

        msg_id = esp_mqtt_client_subscribe(client, "/setTTL", 0);
        ESP_LOGI(TAG_MQTT, "sent subscribe successful, msg_id=%d", msg_id);

        msg_id = esp_mqtt_client_subscribe(client, "/setTN", 0);
        ESP_LOGI(TAG_MQTT, "sent subscribe successful, msg_id=%d", msg_id);

        msg_id = esp_mqtt_client_subscribe(client, "/setTI", 0);
        ESP_LOGI(TAG_MQTT, "sent subscribe successful, msg_id=%d", msg_id);

        msg_id = esp_mqtt_client_subscribe(client, "/setTNWithAddress", 0);
        ESP_LOGI(TAG_MQTT, "sent subscribe successful, msg_id=%d", msg_id);

        msg_id = esp_mqtt_client_subscribe(client, "/setTIWithAddress", 0);
        ESP_LOGI(TAG_MQTT, "sent subscribe successful, msg_id=%d", msg_id);

        msg_id = esp_mqtt_client_subscribe(client, "/setPowerWithAddress", 0);
        ESP_LOGI(TAG_MQTT, "sent subscribe successful, msg_id=%d", msg_id);

        msg_id = esp_mqtt_client_subscribe(client, "/setTTLWithAddress", 0);
        ESP_LOGI(TAG_MQTT, "sent subscribe successful, msg_id=%d", msg_id);

        msg_id = esp_mqtt_client_subscribe(client, "/setAllParameters", 0);
        ESP_LOGI(TAG_MQTT, "sent subscribe successful, msg_id=%d", msg_id);
        break;
    case MQTT_EVENT_DISCONNECTED:
        ESP_LOGI(TAG_MQTT, "MQTT_EVENT_DISCONNECTED");
        MQTT_CONNEECTED=0;
        break;

    case MQTT_EVENT_SUBSCRIBED:
        ESP_LOGI(TAG_MQTT, "MQTT_EVENT_SUBSCRIBED, msg_id=%d", event->msg_id);
        break;
    case MQTT_EVENT_UNSUBSCRIBED:
        ESP_LOGI(TAG_MQTT, "MQTT_EVENT_UNSUBSCRIBED, msg_id=%d", event->msg_id);
        break;
    case MQTT_EVENT_PUBLISHED:
        ESP_LOGI(TAG_MQTT, "MQTT_EVENT_PUBLISHED, msg_id=%d", event->msg_id);
        break;
    case MQTT_EVENT_DATA:
        ESP_LOGI(TAG_MQTT, "MQTT_EVENT_DATA");
        printf("TOPIC=%.*s\r\n", event->topic_len, event->topic);
        printf("DATA=%.*s\r\n", event->data_len, event->data);
        off_all_LED();

        char read_topic[7];
        for(int i = 0; i <= event->topic_len; i++) {
            if(i == event->topic_len) read_topic[i] = '\0';
            else read_topic[i] = event->topic[i];
        }

        if (strcmp(read_topic, "/setTTL") == 0) {
            // Impostare il nuovo valore al nodo client ed inviarlo agli altri nodi
            int read_data;
            sscanf(event->data, "%d", &read_data);
            printf("TTL: %d", read_data);

            if (read_data>=0 && read_data<=7) {
                config_server.default_ttl = read_data;
                uint8_t parametro = 0;
                uint8_t valore = read_data;
                char address[7] = "0xFFFF";
                SendNewParameterValue(parametro, valore, address);
            } else {
                board_led_operation(LED_R, LED_ON);
            }
        } 

        if (strcmp(read_topic, "/setPower") == 0) {
            int read_data;
            sscanf(event->data, "%d", &read_data);
            printf("TP: %d", read_data);

            if (read_data == 1) {
                set_tx_power(ESP_PWR_LVL_N12);
            } else if (read_data == 2){
                set_tx_power(ESP_PWR_LVL_N9);
            } else if (read_data == 3){
                set_tx_power(ESP_PWR_LVL_N6);
            } else if (read_data == 4){
                set_tx_power(ESP_PWR_LVL_N3);
            } else if (read_data == 5){
                set_tx_power(ESP_PWR_LVL_N0);
            } else if (read_data == 6){
                set_tx_power(ESP_PWR_LVL_P3);
            } else if (read_data == 7){
                set_tx_power(ESP_PWR_LVL_P6);
            } else if (read_data == 8){
                set_tx_power(ESP_PWR_LVL_P9);
            } else {
                printf("Si è verificato un errore");
                board_led_operation(LED_R, LED_ON);
            }

            uint8_t parametro = 1;
            uint8_t valore = read_data;
            char address[7] = "0xFFFF";
            SendNewParameterValue(parametro, valore, address);
        }

        if (strcmp(read_topic, "/setTN") == 0) {
            int read_data;
            sscanf(event->data, "%d", &read_data);
            printf("TN: %d", read_data);

            if (read_data>=1 && read_data<=7)  {
                TN = read_data;
                config_server.net_transmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
                config_server.relay_retransmit = ESP_BLE_MESH_TRANSMIT(TN, TI);

                uint8_t parametro = 2;
                uint8_t valore = read_data;
                char address[7] = "0xFFFF";
                SendNewParameterValue(parametro, valore, address);
            } else {
                board_led_operation(LED_R, LED_ON);
            }
        }

        if (strcmp(read_topic, "/setTI") == 0) {
            int read_data;
            sscanf(event->data, "%d", &read_data);
            printf("TI: %d", read_data);

            if (read_data>=20 && read_data<=1000)  {
                TI = read_data;
                config_server.net_transmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
                config_server.relay_retransmit = ESP_BLE_MESH_TRANSMIT(TN, TI);

                uint8_t parametro = 3;
                uint8_t valore = read_data;
                char address[7] = "0xFFFF";
                SendNewParameterValue(parametro, valore, address);
            } else {
                board_led_operation(LED_R, LED_ON);
            }
        }

        if (strcmp(read_topic, "/setTTLWithAddress") == 0) {
            char read_data_string[10];
            strncpy(read_data_string, event->data, event->data_len);
            read_data_string[event->data_len] = '\0';
            printf(read_data_string);
            char* result[10]; // 0: Address     1: valore parametro
            splitString(read_data_string,result);
            printf(" 1: %s", result[0]); 
            printf(" 2: %s", result[1]);
            uint8_t val = atoi(result[1]);
            printf(" 2: %d", val);
            SendNewParameterValue(0, val, result[0]);
        } 

        if (strcmp(read_topic, "/setPowerWithAddress") == 0) {
            char read_data_string[10];
            strncpy(read_data_string, event->data, event->data_len);
            read_data_string[event->data_len] = '\0';
            printf(read_data_string);
            char* result[10]; // 0: Address     1: valore parametro
            splitString(read_data_string,result);
            printf(" 1: %s", result[0]); 
            printf(" 2: %s", result[1]);
            uint8_t val = atoi(result[1]);
            printf(" 2: %d", val);
            SendNewParameterValue(1, val, result[0]);
        }

        if (strcmp(read_topic, "/setTNWithAddress") == 0) {
            char read_data_string[10];
            strncpy(read_data_string, event->data, event->data_len);
            read_data_string[event->data_len] = '\0';
            printf(read_data_string);
            char* result[10]; // 0: Address     1: valore parametro
            splitString(read_data_string,result);
            printf(" 1: %s", result[0]); 
            printf(" 2: %s", result[1]);
            uint8_t val = atoi(result[1]);
            printf(" 2: %d", val);
            SendNewParameterValue(2, val, result[0]);
        }

        if (strcmp(read_topic, "/setTIWithAddress") == 0) {
            char read_data_string[10];
            strncpy(read_data_string, event->data, event->data_len);
            read_data_string[event->data_len] = '\0';
            printf(read_data_string);
            char* result[10]; // 0: Address     1: valore parametro
            splitString(read_data_string,result);
            printf(" 1: %s", result[0]); 
            printf(" 2: %s", result[1]);
            uint8_t val = atoi(result[1]);
            printf(" 2: %d", val);
            SendNewParameterValue(3, val, result[0]);
        }

        if (strcmp(read_topic, "/setAllParameters") == 0) {
             if (Start==FALSE){
                Start = TRUE;
                PDRSend = 0;
                PDRReceived = 0;
            } 
            char read_data_string[10];
            strncpy(read_data_string, event->data, event->data_len);
            read_data_string[event->data_len] = '\0';
            printf(read_data_string);
            char* result[10]; // 0: TTL  1:TP    2:TN    3:TI 
            splitString(read_data_string,result);
            printf(" 0: %s", result[0]); 
            printf(" 1: %s", result[1]);
            printf(" 2: %s", result[2]);
            printf(" 3: %s", result[3]);
            uint8_t TTLval = atoi(result[0]);
            uint8_t TPval = atoi(result[1]);
            uint8_t TNval = atoi(result[2]);
            uint8_t TIval = atoi(result[3]);
            //printf(" 2: %d", val);
            

            if (TTLval>=0 && TTLval<=7 && TPval>=1 && TPval<=8 && TNval>=1 && TNval<=7 && TIval>=1 && TIval<=10) {
                SendNewParameterValue(0, TTLval, "0xFFFF");
                SendNewParameterValue(1, TPval, "0xFFFF");
                SendNewParameterValue(2, TNval, "0xFFFF");
                SendNewParameterValue(3, TIval, "0xFFFF");

                if (TTLval == 1) {
                    TI = 20;
                    config_server.net_transmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
                    config_server.relay_retransmit = ESP_BLE_MESH_TRANSMIT(TN, TI);

                    uint8_t parametro = 3;
                    uint8_t valore = TTLval;
                    char address[7] = "0xFFFF";
                    SendNewParameterValue(parametro, valore, address);
                } else if (TTLval == 2) {
                    TI = 100;
                    config_server.net_transmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
                    config_server.relay_retransmit = ESP_BLE_MESH_TRANSMIT(TN, TI);

                    uint8_t parametro = 3;
                    uint8_t valore = TTLval;
                    char address[7] = "0xFFFF";
                    SendNewParameterValue(parametro, valore, address);
                } else if (TTLval == 3) {
                    TI = 250;
                    config_server.net_transmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
                    config_server.relay_retransmit = ESP_BLE_MESH_TRANSMIT(TN, TI);

                    uint8_t parametro = 3;
                    uint8_t valore = TTLval;
                    char address[7] = "0xFFFF";
                    SendNewParameterValue(parametro, valore, address);
                } else if (TTLval == 4) {
                    TI = 500;
                    config_server.net_transmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
                    config_server.relay_retransmit = ESP_BLE_MESH_TRANSMIT(TN, TI);

                    uint8_t parametro = 3;
                    uint8_t valore = TTLval;
                    char address[7] = "0xFFFF";
                    SendNewParameterValue(parametro, valore, address);
                } else if (TTLval == 5) {
                    TI = 1000;
                    config_server.net_transmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
                    config_server.relay_retransmit = ESP_BLE_MESH_TRANSMIT(TN, TI);

                    uint8_t parametro = 3;
                    uint8_t valore = TTLval;
                    char address[7] = "0xFFFF";
                    SendNewParameterValue(parametro, valore, address);
                } else {
                    board_led_operation(LED_R, LED_ON);
                }

                if (TPval == 1) {
                    set_tx_power(ESP_PWR_LVL_N12);
                } else if (TPval == 2){
                    set_tx_power(ESP_PWR_LVL_N9);
                } else if (TPval == 3){
                    set_tx_power(ESP_PWR_LVL_N6);
                } else if (TPval == 4){
                    set_tx_power(ESP_PWR_LVL_N3);
                } else if (TPval == 5){
                    set_tx_power(ESP_PWR_LVL_N0);
                } else if (TPval == 6){
                    set_tx_power(ESP_PWR_LVL_P3);
                } else if (TPval == 7){
                    set_tx_power(ESP_PWR_LVL_P6);
                } else if (TPval == 8){
                    set_tx_power(ESP_PWR_LVL_P9);
                }

                TN = TNval;
                config_server.net_transmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
                config_server.relay_retransmit = ESP_BLE_MESH_TRANSMIT(TN, TI);

                TI = TIval;
                config_server.net_transmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
                config_server.relay_retransmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
                
            } else {
                board_led_operation(LED_R, LED_ON);
            }
        }
            
        break;
    case MQTT_EVENT_ERROR:
        ESP_LOGI(TAG_MQTT, "MQTT_EVENT_ERROR");
        break;
    default:
        ESP_LOGI(TAG_MQTT, "Other event id:%d", event->event_id);
        break;
    }
}


static void mqtt_app_start(void)
{
    ESP_LOGI(TAG_MQTT, "STARTING MQTT");
    esp_mqtt_client_config_t mqttConfig = {
        .uri = "mqtt:"};
    
    client = esp_mqtt_client_init(&mqttConfig);
    esp_mqtt_client_register_event(client, ESP_EVENT_ANY_ID, mqtt_event_handler, client);
    esp_mqtt_client_start(client);
}

void app_main(void)
{
    esp_err_t err;

    ESP_LOGI(TAG, "Initializing...");

    board_init();

    err = nvs_flash_init();
    if (err == ESP_ERR_NVS_NO_FREE_PAGES) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        err = nvs_flash_init();
    }
    ESP_ERROR_CHECK(err);

    wifi_init();

    err = bluetooth_init();
    if (err) {
        ESP_LOGE(TAG, "esp32_bluetooth_init failed (err %d)", err);
        return;
    }

    /* Open nvs namespace for storing/restoring mesh example info */
    err = ble_mesh_nvs_open(&NVS_HANDLE);
    if (err) {
        return;
    }

    ble_mesh_get_dev_uuid(dev_uuid);

    /* Initialize the Bluetooth Mesh Subsystem */
    err = ble_mesh_init();
    if (err) {
        ESP_LOGE(TAG, "Bluetooth mesh init failed (err %d)", err);
    }

    while (true) {
        ESP_LOGI(TAG, "PDRSend %d", PDRSend);
        if (PDRSend <= 50) {
            vTaskDelay(2500 / portTICK_PERIOD_MS);
            example_ble_mesh_send_gen_onoff_set2();
        } else {
            vTaskDelay(50000 / portTICK_PERIOD_MS);
            if (Start==FALSE){
                PDRSend = 0;
                PDRReceived = 0;
            } else if(PDRSend != 0) {
                ESP_LOGI(TAG, "PDRReceived %d", PDRReceived);
                ESP_LOGI(TAG, "PDRSend %d", PDRSend);
                char PDR[5];
                sprintf(PDR, "%d-%d", PDRSend, PDRReceived);
                printf(PDR);
                if(MQTT_CONNEECTED) {
                    esp_mqtt_client_publish(client, "/sendPDR",  PDR, 0, 0, 0);
                }

                PDRSend = 0;
                PDRReceived = 0;
            }
            if(MQTT_CONNEECTED) {
                esp_mqtt_client_publish(client, "/getNewParameters",  "1", 0, 0, 0);
            }
        }
    }
    
}