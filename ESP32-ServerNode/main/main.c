/* main.c - Application main entry point */

/*
 * SPDX-FileCopyrightText: 2017 Intel Corporation
 * SPDX-FileContributor: 2018-2021 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <stdio.h>
#include <string.h>

#include "esp_log.h"
#include "nvs_flash.h"

#include "esp_ble_mesh_defs.h"
#include "esp_ble_mesh_common_api.h"
#include "esp_ble_mesh_networking_api.h"
#include "esp_ble_mesh_provisioning_api.h"
#include "esp_ble_mesh_config_model_api.h"
#include "esp_ble_mesh_generic_model_api.h"
#include "esp_ble_mesh_local_data_operation_api.h"

#include "board.h"
#include "ble_mesh_example_init.h"

#include <esp_bt.h>

static uint8_t nodeID = 1;
#define MAX_RETRY 10
//static int retry_cnt = 0;



static esp_ble_mesh_client_t onoff_client;
static struct example_info_store {
    uint16_t net_idx;   /* NetKey Index */
    uint16_t app_idx;   /* AppKey Index */
    uint8_t  onoff;     /* Remote OnOff */
    uint8_t  tid;       /* Message TID */
} __attribute__((packed)) store = {
    .net_idx = ESP_BLE_MESH_KEY_UNUSED,
    .app_idx = ESP_BLE_MESH_KEY_UNUSED,
    .onoff = 0x4,
    .tid = 0x0,
};

#define TAG "BLE Mesh"
#define CID_ESP 0x02E5
extern struct _led_state led_state[3];
static uint8_t dev_uuid[16] = { 0xdd, 0xdd };

esp_ble_mesh_cfg_srv_t config_server = {
    .relay = ESP_BLE_MESH_RELAY_ENABLED,
    .relay_retransmit = ESP_BLE_MESH_TRANSMIT(2, 20),
    .beacon = ESP_BLE_MESH_BEACON_ENABLED,
    .gatt_proxy = ESP_BLE_MESH_GATT_PROXY_NOT_SUPPORTED,
    .default_ttl = 7,
    .net_transmit = ESP_BLE_MESH_TRANSMIT(2, 20)
};
uint16_t TN = 2;
uint16_t TI = 20;

ESP_BLE_MESH_MODEL_PUB_DEFINE(onoff_pub_0, 2 + 3, ROLE_NODE);
static esp_ble_mesh_gen_onoff_srv_t onoff_server_0 = {
    .rsp_ctrl.get_auto_rsp = ESP_BLE_MESH_SERVER_AUTO_RSP,
    .rsp_ctrl.set_auto_rsp = ESP_BLE_MESH_SERVER_AUTO_RSP,
};

ESP_BLE_MESH_MODEL_PUB_DEFINE(onoff_pub_1, 2 + 3, ROLE_NODE);
static esp_ble_mesh_gen_onoff_srv_t onoff_server_1 = {
    .rsp_ctrl.get_auto_rsp = ESP_BLE_MESH_SERVER_RSP_BY_APP,
    .rsp_ctrl.set_auto_rsp = ESP_BLE_MESH_SERVER_RSP_BY_APP,
};

ESP_BLE_MESH_MODEL_PUB_DEFINE(onoff_pub_2, 2 + 3, ROLE_NODE);
static esp_ble_mesh_gen_onoff_srv_t onoff_server_2 = {
    .rsp_ctrl.get_auto_rsp = ESP_BLE_MESH_SERVER_AUTO_RSP,
    .rsp_ctrl.set_auto_rsp = ESP_BLE_MESH_SERVER_RSP_BY_APP,
};

static esp_ble_mesh_model_t root_models[] = {
    ESP_BLE_MESH_MODEL_CFG_SRV(&config_server),
    ESP_BLE_MESH_MODEL_GEN_ONOFF_SRV(&onoff_pub_0, &onoff_server_0),
};

static esp_ble_mesh_model_t extend_model_0[] = {
    ESP_BLE_MESH_MODEL_GEN_ONOFF_SRV(&onoff_pub_1, &onoff_server_1),
};

static esp_ble_mesh_model_t extend_model_1[] = {
    ESP_BLE_MESH_MODEL_GEN_ONOFF_SRV(&onoff_pub_2, &onoff_server_2),
};

static esp_ble_mesh_elem_t elements[] = {
    ESP_BLE_MESH_ELEMENT(0, root_models, ESP_BLE_MESH_MODEL_NONE),
    ESP_BLE_MESH_ELEMENT(0, extend_model_0, ESP_BLE_MESH_MODEL_NONE),
    ESP_BLE_MESH_ELEMENT(0, extend_model_1, ESP_BLE_MESH_MODEL_NONE),
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

static void prov_complete(uint16_t net_idx, uint16_t addr, uint8_t flags, uint32_t iv_index)
{
    ESP_LOGI(TAG, "net_idx: 0x%04x, addr: 0x%04x", net_idx, addr);
    ESP_LOGI(TAG, "flags: 0x%02x, iv_index: 0x%08x", flags, iv_index);
    board_led_operation(LED_G, LED_OFF);
}

static void example_change_led_state(esp_ble_mesh_model_t *model,
                                     esp_ble_mesh_msg_ctx_t *ctx, uint8_t onoff)
{
    uint16_t primary_addr = esp_ble_mesh_get_primary_element_address();
    uint8_t elem_count = esp_ble_mesh_get_element_count();
    struct _led_state *led = NULL;
    uint8_t i;

    if (ESP_BLE_MESH_ADDR_IS_UNICAST(ctx->recv_dst)) {
        for (i = 0; i < elem_count; i++) {
            if (ctx->recv_dst == (primary_addr + i)) {
                led = &led_state[i];
                board_led_operation(led->pin, onoff);
            }
        }
    } else if (ESP_BLE_MESH_ADDR_IS_GROUP(ctx->recv_dst)) {
        if (esp_ble_mesh_is_model_subscribed_to_group(model, ctx->recv_dst)) {
            led = &led_state[model->element->element_addr - primary_addr];
            board_led_operation(led->pin, onoff);
        }
    } else if (ctx->recv_dst == 0xFFFF) {
        led = &led_state[model->element->element_addr - primary_addr];
        board_led_operation(led->pin, onoff);
    }
}

static void example_handle_gen_onoff_msg(esp_ble_mesh_model_t *model,
                                         esp_ble_mesh_msg_ctx_t *ctx,
                                         esp_ble_mesh_server_recv_gen_onoff_set_t *set)
{
    esp_ble_mesh_gen_onoff_srv_t *srv = model->user_data;
    printf("SONO QUI invio il messaggio?");
    ESP_LOGI(TAG, "TEST 0x%04x", set->op_en);
    ESP_LOGI(TAG, "TTLRECV 0x%04x", ctx->recv_ttl);
    switch (ctx->recv_op) {
        

    case ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_GET:
        esp_ble_mesh_server_model_send_msg(model, ctx,
            ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_STATUS, sizeof(srv->state.onoff), &srv->state.onoff);
        break;
    case ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_SET:
        break;
    case ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_SET_UNACK:
        ESP_LOGI(TAG, "TTLRECV 0x%04x", ctx->recv_ttl);
        uint8_t TTLResidue = (uint8_t)ctx->recv_ttl;
        TTLResidue = TTLResidue - 2;
        uint8_t MessageId = (uint8_t)set->op_en;
        ESP_LOGI(TAG, "MessageID %d", MessageId);
        uint8_t combinazione = (nodeID & 0x03) << 6;   // i primi due bit di nodeID spostati a sinistra di 6 posizioni
        ESP_LOGI(TAG, "Combinazione NodeId %d", combinazione);
        combinazione |= (TTLResidue & 0x03) << 4;     // i successivi due bit di TTLResidue spostati a sinistra di 4 posizioni e combinati con gli altri due bit di nodeID
        ESP_LOGI(TAG, "Combinazione TTL Redisuo %d", combinazione);
        combinazione |= (MessageId & 0x0F);           // gli ultimi 4 bit di messageID combinati con i primi quattro bit di combinazione
        ESP_LOGI(TAG, "Combinazione %d", combinazione);

        esp_ble_mesh_server_model_send_msg(model, ctx,
            ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_STATUS, sizeof(combinazione), &combinazione);
        break;
    default:
        break;
    }
}

static void example_ble_mesh_provisioning_cb(esp_ble_mesh_prov_cb_event_t event,
                                             esp_ble_mesh_prov_cb_param_t *param)
{
    switch (event) {
    case ESP_BLE_MESH_PROV_REGISTER_COMP_EVT:
        ESP_LOGI(TAG, "ESP_BLE_MESH_PROV_REGISTER_COMP_EVT, err_code %d", param->prov_register_comp.err_code);
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
        ESP_LOGI(TAG, "ESP_BLE_MESH_NODE_PROV_RESET_EVT");
        break;
    case ESP_BLE_MESH_NODE_SET_UNPROV_DEV_NAME_COMP_EVT:
        ESP_LOGI(TAG, "ESP_BLE_MESH_NODE_SET_UNPROV_DEV_NAME_COMP_EVT, err_code %d", param->node_set_unprov_dev_name_comp.err_code);
        break;
    default:
        break;
    }
}


esp_err_t set_tx_power(esp_power_level_t power_level) {
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

static void setParameterFunction(uint8_t parametro, uint8_t valore){
    ESP_LOGI(TAG, "Parametro %d", parametro);
    ESP_LOGI(TAG, "Valore %d", valore);

    switch(parametro) {
        case 0:
            printf("Hai scelto la opzione 0 - TTL.\n");
            if (valore>=0 && valore<=7) {
                config_server.default_ttl = valore;
            } else {
                board_led_operation(LED_R, LED_ON);
            }
            break;
        case 1:
            printf("Hai scelto la opzione 1 - PT.\n");
            switch (valore) {
                case 1:
                    set_tx_power(ESP_PWR_LVL_N12);
                    break;
                case 2:
                    set_tx_power(ESP_PWR_LVL_N9);
                    break;
                case 3:
                    set_tx_power(ESP_PWR_LVL_N6);
                    break;
                case 4:
                    set_tx_power(ESP_PWR_LVL_N3);
                    break;
                case 5:
                    set_tx_power(ESP_PWR_LVL_N0);
                    break;
                case 6:
                    set_tx_power(ESP_PWR_LVL_P3);
                    break;
                case 7:
                    set_tx_power(ESP_PWR_LVL_P6);
                    break;
                case 8:
                    set_tx_power(ESP_PWR_LVL_P9);
                    break;
                default:
                    board_led_operation(LED_R, LED_ON);
                    break;
            }

            break;
        case 2:
            printf("Hai scelto la opzione 2 - TN.\n");
            if (valore>=1 && valore<=7)  {
                TN = valore;
                config_server.net_transmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
                config_server.relay_retransmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
            } else {
                board_led_operation(LED_R, LED_ON);
            }
            break;
        case 3:
            printf("Hai scelto la opzione 3 - TI.\n");
            if (valore == 1) {
                TI = 20;
                config_server.net_transmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
                config_server.relay_retransmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
            } else if (valore == 2) {
                TI = 100;
                config_server.net_transmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
                config_server.relay_retransmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
            } else if (valore == 3) {
                TI = 250;
                config_server.net_transmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
                config_server.relay_retransmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
            } else if (valore == 4) {
                TI = 500;
                config_server.net_transmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
                config_server.relay_retransmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
            } else if (valore == 5) {
                TI = 1000;
                config_server.net_transmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
                config_server.relay_retransmit = ESP_BLE_MESH_TRANSMIT(TN, TI);
            } else {
                board_led_operation(LED_R, LED_ON);
            }
            break;
        default:
            printf("Si è verificato un errore.\n");
            break;
    }
}

static void example_ble_mesh_generic_server_cb(esp_ble_mesh_generic_server_cb_event_t event,
                                               esp_ble_mesh_generic_server_cb_param_t *param)
{
    esp_ble_mesh_gen_onoff_srv_t *srv = param->model->user_data;
	esp_ble_mesh_generic_server_cb_param_t *paramResent = { 0 };
	printf("----\n");

    switch (event) {
    case ESP_BLE_MESH_GENERIC_SERVER_STATE_CHANGE_EVT:
        printf("SONO QUI 1 ");
        ESP_LOGI(TAG, "ESP_BLE_MESH_GENERIC_SERVER_STATE_CHANGE_EVT");
        if (param->ctx.recv_op == ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_SET ||
            param->ctx.recv_op == ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_SET_UNACK) {

            printf("SONO QUI 17-03-2023");
            uint8_t parametroValore = param->value.set.onoff.op_en;
            uint8_t identificatore = (parametroValore & 0x80) >> 7;
            uint8_t idMessaggio, parametro, valore;

            if (identificatore == 0) {
                idMessaggio = parametroValore & 0x7F;
                parametro = 0;
                valore = 0;
                example_handle_gen_onoff_msg(param->model, &param->ctx,  &param->value.set);
            } else {
                parametro = (parametroValore & 0x60) >> 5;
                valore = parametroValore & 0x1F;
                idMessaggio = 0;
                setParameterFunction(parametro, valore);
            }

            ESP_LOGI(TAG, "identificatore 0x%d", identificatore);
            ESP_LOGI(TAG, "idMessaggio 0x%d", idMessaggio);
            ESP_LOGI(TAG, "parametro 0x%d", parametro);
            ESP_LOGI(TAG, "valore 0x%d", valore);
        }
        break;
    case ESP_BLE_MESH_GENERIC_SERVER_RECV_GET_MSG_EVT:
    printf("SONO QUI 2");
        ESP_LOGI(TAG, "ESP_BLE_MESH_GENERIC_SERVER_RECV_GET_MSG_EVT");
        if (param->ctx.recv_op == ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_GET) {
            srv = param->model->user_data;
            ESP_LOGI(TAG, "onoff 0x%02x", srv->state.onoff);
            example_handle_gen_onoff_msg(param->model, &param->ctx, NULL);
        }
        break;
    case ESP_BLE_MESH_GENERIC_SERVER_RECV_SET_MSG_EVT:
        printf("SONO QUI 3");
        ESP_LOGI(TAG, "ESP_BLE_MESH_GENERIC_SERVER_RECV_SET_MSG_EVT");
        if (param->ctx.recv_op == ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_SET ||
            param->ctx.recv_op == ESP_BLE_MESH_MODEL_OP_GEN_ONOFF_SET_UNACK) {
            ESP_LOGI(TAG, "onoff 0x%02x, tid 0x%02x", param->value.set.onoff.onoff, param->value.set.onoff.tid);

            if (param->value.set.onoff.op_en) {
                ESP_LOGI(TAG, "trans_time 0x%02x, delay 0x%02x",
                    param->value.set.onoff.trans_time, param->value.set.onoff.delay);
            }
            example_handle_gen_onoff_msg(param->model, &param->ctx, &param->value.set.onoff);
        }
        break;
    
    default:
        ESP_LOGE(TAG, "Unknown Generic Server event 0x%02x", event);
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
            break;
        case ESP_BLE_MESH_MODEL_OP_MODEL_SUB_ADD:
            ESP_LOGI(TAG, "ESP_BLE_MESH_MODEL_OP_MODEL_SUB_ADD");
            ESP_LOGI(TAG, "elem_addr 0x%04x, sub_addr 0x%04x, cid 0x%04x, mod_id 0x%04x",
                param->value.state_change.mod_sub_add.element_addr,
                param->value.state_change.mod_sub_add.sub_addr,
                param->value.state_change.mod_sub_add.company_id,
                param->value.state_change.mod_sub_add.model_id);
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
    esp_ble_mesh_register_config_server_callback(example_ble_mesh_config_server_cb);
    esp_ble_mesh_register_generic_server_callback(example_ble_mesh_generic_server_cb);

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

void off_all_LED(){
    board_led_operation(LED_G, LED_OFF);
    board_led_operation(LED_R, LED_OFF);
    board_led_operation(LED_B, LED_OFF);
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

    err = bluetooth_init();
    if (err) {
        ESP_LOGE(TAG, "esp32_bluetooth_init failed (err %d)", err);
        return;
    }

    ble_mesh_get_dev_uuid(dev_uuid);

    /* Initialize the Bluetooth Mesh Subsystem */
    err = ble_mesh_init();
    if (err) {
        ESP_LOGE(TAG, "Bluetooth mesh init failed (err %d)", err);
    }
}