import logging
import time

from src.lib.util.generator import Generations
from src.lib.constant.header import *
from src.v187.entity.credential import CredentialCustom


class Header(CredentialCustom, Generations):
    CONNECTION = 'WIFI'
    FACEBOOK_ANALYTICS_APPLICATION_ID = '567067343352427'
    EXPERIMENTS = "ig_growth_android_profile_pic_prefill_with_fb_pic_2,ig_account_identity_logged_out_signals_global_holdout_universe,ig_android_caption_typeahead_fix_on_o_universe,ig_android_retry_create_account_universe,ig_android_gmail_oauth_in_reg,ig_android_quickcapture_keep_screen_on,ig_android_smartlock_hints_universe,ig_android_reg_modularization_universe,ig_android_login_identifier_fuzzy_match,ig_android_passwordless_account_password_creation_universe,ig_android_security_intent_switchoff,ig_android_sim_info_upload,ig_android_device_verification_fb_signup,ig_android_reg_nux_headers_cleanup_universe,ig_android_direct_main_tab_universe_v2,ig_android_nux_add_email_device,ig_android_fb_account_linking_sampling_freq_universe,ig_android_device_info_foreground_reporting,ig_android_suma_landing_page,ig_android_device_verification_separate_endpoint,ig_android_direct_add_direct_to_android_native_photo_share_sheet,ig_android_device_detection_info_upload,ig_android_device_based_country_verification"

    def __init__(self, logger: logging, salt: str):
        self.__log = logger
        self.__log.debug('Start Header')
        CredentialCustom.__init__(self, logger, '1', '2', '3')
        Generations.__init__(self, logger, salt)

    def default(self):
        return self.__default

    def authorized(self):
        return {**self.__default, **{
            'Authorization': self.bearer,
            IG_U_RUR: self.u_rur,
            IG_U_DS_USER_ID: str(self.user_id),
            X_IG_Timezone_Offset: str(-3 * 3600)
        }}

    @property
    def __default(self):
        return {
            X_IG_App_Locale: self.language,
            X_IG_Device_Locale: self.language,
            X_IG_Mapped_Locale: self.language,
            X_Pigeon_Session_Id: self.pigeon_session_id(self.username),
            X_Pigeon_Rawclienttime: '{}'.format(round(time.time(), 3)),
            X_IG_Bandwidth_Speed_KBPS: '-1 kbps',
            X_IG_Bandwidth_TotalBytes_B: '0',
            X_IG_Bandwidth_TotalTime_MS: '0',
            X_Bloks_Version_Id: self.bloks_version_id,
            X_IG_WWW_Claim: self.claim,
            X_Bloks_Is_Layout_RTL: 'false',
            X_Bloks_Is_Panorama_Enabled: 'false',
            X_IG_Device_ID: self.guid_id(self.username),
            X_IG_Family_Device_ID: self.family_guid_id(self.username),
            X_IG_Android_ID: self.android_id(self.username),
            X_IG_App_ID: self.FACEBOOK_ANALYTICS_APPLICATION_ID,
            User_Agent: self.user_agent,
            Accept_Language: self.language,
            X_MID: self.mid,
            IG_INTENDED_USER_ID: str(self.user_id) if self.user_id else "0",
            Content_Type: 'application/x-www-form-urlencoded; charset=UTF-8',
            Accept_Encoding: 'gzip, deflate',
            Host: 'i.instagram.com',
            X_FB_HTTP_Engine: 'Liger',
            X_FB_Client_IP: 'True',
            X_FB_Server_Cluster: 'True',
            Connection: 'close'
        }
