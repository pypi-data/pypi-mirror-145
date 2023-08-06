import time

from src.InstagramFakeAPI.lib.util.generator import Generations
from src.InstagramFakeAPI.v159.entity.credential import CredentialCustom


class Header(CredentialCustom, Generations):
    CONNECTION = 'WIFI'
    FACEBOOK_ORCA_APPLICATION_ID = '124024574287414'
    FACEBOOK_ANALYTICS_APPLICATION_ID = '567067343352427'
    EXPERIMENTS = "ig_growth_android_profile_pic_prefill_with_fb_pic_2,ig_account_identity_logged_out_signals_global_holdout_universe,ig_android_caption_typeahead_fix_on_o_universe,ig_android_retry_create_account_universe,ig_android_gmail_oauth_in_reg,ig_android_quickcapture_keep_screen_on,ig_android_smartlock_hints_universe,ig_android_reg_modularization_universe,ig_android_login_identifier_fuzzy_match,ig_android_passwordless_account_password_creation_universe,ig_android_security_intent_switchoff,ig_android_sim_info_upload,ig_android_device_verification_fb_signup,ig_android_reg_nux_headers_cleanup_universe,ig_android_direct_main_tab_universe_v2,ig_android_nux_add_email_device,ig_android_fb_account_linking_sampling_freq_universe,ig_android_device_info_foreground_reporting,ig_android_suma_landing_page,ig_android_device_verification_separate_endpoint,ig_android_direct_add_direct_to_android_native_photo_share_sheet,ig_android_device_detection_info_upload,ig_android_device_based_country_verification"

    def __init__(self, salt: str):
        self.__log.debug('Start Header')
        CredentialCustom.__init__(self, '1', '2', '3')
        Generations.__init__(self, salt)
        # self.__mid = ''

    # def last_connection_auth(self):
    #     return {
    #         'cookie': self.cookies,
    #         'claim': self.__claim,
    #         'ig-set-authorization': self.__bearer
    #     }

    def default(self):
        return self.__default

    # def authorized(self):
    #     return {**self.__default, **{'Authorization': self.__bearer}}

    def authorized(self):
        return {
            **self.__default,
            **{'Cookie': "; ".join([str(x) + "=" + str(y) for x, y in self.cookies.items()])},
            }

    @property
    def __default(self):
        return {
            'X-IG-App-Locale': self.language,
            'X-IG-Device-Locale': self.language,
            'X-IG-Mapped-Locale': self.language,
            'X-Pigeon-Session-Id': self.pigeon_session_id(self.username),
            'X-Pigeon-Rawclienttime': '{}'.format(round(time.time(), 3)),
            'X-IG-Connection-Speed': '-1 kbps',
            'X-IG-Bandwidth-Speed-KBPS': '-1.000',
            'X-IG-Bandwidth-TotalBytes-B': '0',
            'X-IG-Bandwidth-TotalTime-MS': '0',
            'X-Bloks-Version-Id': self.bloks_version_id,
            'X-IG-WWW-Claim': self.claim,
            'X-Bloks-Is-Layout-RTL': 'false',
            'X-Bloks-Is-Panorama-Enabled': 'false',
            # 'X-IG-Family-Device-ID': self.phone_id(self.username),
            'X-IG-Device-ID': self.guid_id(self.username),
            'X-IG-Android-ID': self.android_id(self.username),
            # 'X-IG-Timezone-Offset': str(-4 * 3600),
            'X-IG-Connection-Type': self.connection_type_header if self.connection_type_header else self.CONNECTION,
            'X-IG-Capabilities': self.capabilities,
            # 'X-IG-App-Startup-Country': 'RU',
            # 'X-IG-Nav-Chain': '3vd:login_landing:3',
            # 'Priority': 'u=3',
            'X-IG-App-ID': self.FACEBOOK_ANALYTICS_APPLICATION_ID,
            'User-Agent': self.user_agent,
            'Accept-Language': self.language.replace('_', '-'),
            # 'X-MID': self.mid,
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'i.instagram.com',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-FB-HTTP-Engine': 'Liger',
            # 'X-FB-Client-IP': 'True',
            # 'X-FB-Server-Cluster': 'True',
            'Connection': 'close',
        }

    # @property
    # def mid(self):
    #     return self.extract_cookie('mid') if len(self.extract_cookie('mid')) else self.__mid
    #
    # @mid.setter
    # def mid(self, value: str):
    #     self.__mid = value

    # @property
    # def __bearer(self) -> str:
    #     return self.bearer if self.bearer else self.extract_header('ig-set-authorization')

    # @property
    # def __claim(self) -> str:
    #     result = self.claim if self.claim else self.extract_header('x-ig-set-www-claim')
    #     return result if result else '0'
