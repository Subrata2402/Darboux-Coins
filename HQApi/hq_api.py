import json, jwt, aiohttp, asyncio
from HQApi.exceptions import ApiResponseError, BannedIPError

class BaseHQApi:
    def __init__(self, token: str = None, login_token: str = None):
        self.token = token
        self.login_token = login_token

    async def api(self):
        return self

    async def get_users_me(self):
        """
        Get details of a user.
        response_data = {
                    'achievementCount': 0,
                    'avatarUrl': 'https://cdn.prod.hype.space/da/gold.png',
                    'blocked': False,
                    'blocksMe': False,
                    'broadcasts': {'data': []},
                    'coins': 678,
                    'created': '2021-03-23T02:35:38.000Z',
                    'deviceTokens': [],
                    'erase1s': 0,
                    'featured': False,
                    'friendIds': [],
                    'gamesPlayed': 12,
                    'hasPhone': True,
                    'highScore': 0,
                    'identities': [],
                    'items': {'erase1s': 0, 'lives': 2, 'popularChoices': None, 'superSpins': 0},
                    'leaderboard': {
                                'alltime': {'rank': 101, 'total': '$0', 'wins': 0},
                                'rank': 101,
                                'total': '$0',
                                'totalCents': 0,
                                'unclaimed': '$0',
                                'weekly': {'rank': 101, 'total': '$0', 'wins': 0},
                                'wins': 0
                    },
                    'lives': 2,
                    'phoneNumber': '+447404447991',
                    'preferences': {'hq-general': True, 'sharingEnabled': True},
                    'referralUrl': 'https://hqtrivia.com/i/HelmaKai95',
                    'referred': True,
                    'referringUserId': 27015094,
                    'stk': 'Mg==',
                    'streakInfo': {
                            'current': 0,
                            'lastPlayed': '2022-03-28T21:40:42.327Z',
                            'lifeUuid': None,
                            'notify': True,
                            'startDate': '2022-03-28T07:00:00.000Z',
                            'target': 5,
                            'total': 0,
                            'userId': 27353247
                    },
                    'userId': 27353247,
                    'username': 'HelmaKai95',
                    'voip': False,
                    'winCount': 0
                }
        """
        return await self.fetch("GET", "users/me")

    async def get_user(self, id: str):
        """
        Get a HQ user details.
        response_data = {
                'achievementCount': 0,
                'avatarUrl': 'https://prd-bucket-hqtrivia-01012022.nyc3.cdn.digitaloceanspaces.com/da/gold.png',
                'blocked': False,
                'blocksMe': False,
                'broadcasts': {'data': []},
                'created': '2020-12-23T16:22:00.000Z',
                'featured': False,
                'gamesPlayed': 0,
                'highScore': 0,
                'leaderboard': {
                    'alltime': {'rank': 101, 'total': '$0', 'wins': 0},
                    'rank': 101,
                    'total': '$0',
                    'totalCents': 0,
                    'unclaimed': '$0',
                    'weekly': {'rank': 101, 'total': '$0', 'wins': 0},
                    'wins': 0
                },
                'referralUrl': 'https://hqtrivia.com/i/ntzamos',
                'userId': 27196172,
                'username': 'ntzamos',
                'winCount': 0
        }
        """
        return await self.fetch("GET", "users/{}".format(id))

    async def search(self, name):
        """
        Search a HQ user.
        response_data = {
            'data': [{
                'avatarUrl': 'https://cdn.prod.hype.space/da/purple.png',
                'created': '2020-06-02T02:41:50.000Z',
                'featured': False,
                'lastLive': None,
                'live': False,
                'subscriberCount': 0,
                'userId': '26755116',
                'username': 'josephine3250'
            },
            {
                'avatarUrl': 'https://cdn.prod.hype.space/da/blue.png',
                'created': '2021-05-24T06:07:00.000Z',
                'featured': False,
                'lastLive': None,
                'live': False,
                'subscriberCount': 0,
                'userId': '27480572',
                'username': 'Josephine3250fb'
            }],
            'links': {
                'next': None,
                'prev': '/users?q=Josephine3250&before=1',
                'self': '/users?q=Josephine3250'
                }
            }
        """
        return await self.fetch("GET", 'users?q={}'.format(name))

    async def get_payouts_me(self):
        """
        Get payout details.
        response_data = {
                    'balance': {
                        'appealStatus': 'none',
                        'available': '$0',
                        'documentRequired': False,
                        'documentStatus': 'none',
                        'eligibleForPayout': False,
                        'frozen': '$0',
                        'hasPending': False,
                        'paid': '$10.50',
                        'payoutEligibility': 'disallowed_not_enough',
                        'payoutsConnected': True,
                        'payoutsEmail': 'sakhman2001@gmail.com',
                        'pending': '$0',
                        'prizeTotal': '$10.50',
                        'unpaid': '$0',
                        'winsReadyForCashout': True
                    },
                    'charities': [{
                        'charityIconUrl': 'https://cdn.prod.hype.space/charity-icons/7692404-A1IHqy',
                        'charityId': 'ckfbjy9qp0000015a2u78gl3k',
                        'displayName': "Tuesday's Children"
                    },
                    {
                        'charityIconUrl': 'https://cdn.prod.hype.space/charity-icons/7692404-mkzp4p',
                        'charityId': 'ckfbjxf7d0000011ubxtq2s6p',
                        'displayName': 'Rock the Vote'
                    }],
                    'payouts': [{
                        'amount': '$1.88',
                        'created': '2021-05-03T01:43:02.000Z',
                        'currency': 'USD',
                        'metadata': {
                                'batchId': 'KC2ZUQES5NTKE',
                                'client': 'Android/1.49.8',
                                'ipAddress': '54.242.1.233',
                                'payoutsConnected': True,
                                'senderBatchId': 'payout_4827411'
                            },
                        'modified': '2021-05-03T01:47:59.000Z',
                        'payoutId': 4827411,
                        'status': 10001,
                        'targetEmail': 'sakhman2001@gmail.com',
                        'targetPhone': None,
                        'targetUserId': None,
                        'userId': 27232225
                    },
                    {
                        'amount': '$0.79',
                        'created': '2021-04-07T03:03:47.000Z',
                        'currency': 'USD',
                        'metadata': {
                                'batchId': '88ULYQXB74SME',
                                'client': 'Android/1.49.8',
                                'ipAddress': '35.175.205.12',
                                'payoutsConnected': True,
                                'senderBatchId': 'payout_4815149'
                            },
                        'modified': '2021-04-13T16:26:17.000Z',
                        'payoutId': 4815149,
                        'status': 10001,
                        'targetEmail': 'sakhman2001@gmail.com',
                        'targetPhone': None,
                        'targetUserId': None,
                        'userId': 27232225
                    },
                ]}
        """
        return await self.fetch("GET", "users/me/payouts")

    async def get_show(self):
        """
        Get HQ show details.
        response_data = {
                    'active': False,
                    'atCapacity': False,
                    'broadcast': None,
                    'broadcastFull': False,
                    'gameType': None,
                    'media': None,
                    'nextGameType': 'trivia',
                    'nextShowPrize': '$1,500',
                    'nextShowTime': '2022-04-01T01:00:00.000Z',
                    'nextShowVertical': 'general',
                    'prize': None,
                    'prizePoints': None,
                    'showId': None,
                    'showType': None,
                    'startTime': None,
                    'upcoming': [{
                            'gameType': 'trivia',
                            'media': [],
                            'nextShowLabel': {'color': '#FFFFFF', 'title': 'HQ Trivia'},
                            'optIn': {'color': '#FFFFFF', 'opt': 'hq-general'},
                            'prize': '$1,500',
                            'showType': 'hq',
                            'time': '2022-04-01T01:00:00.000Z',
                            'vertical': 'general'}
                        ]}
        """
        return await self.fetch("GET", "shows/now")

    async def get_schedule(self):
        """
        Get HQ schedule.
        response_data = {
                    'announcements': [],
                    'offairTrivia': {
                                'games': [{
                                    'answerResults': [True],
                                    'category': 'TV',
                                    'gameUuid': 'cl17nlnqc07vx01i98jpjfr3b',
                                    'questionCount': 12,
                                    'questionNumber': 2,
                                    'reminders': [{
                                            'message': 'Complete your Daily '
                                                        'Challenge now before '
                                                        'it’s too late!',
                                            'sendMs': 14400000}],
                                    'status': 'question_answered'}],
                                'isGameInProgress': True,
                                'powerups': {
                                    'OFFAIR_PTS_MULTI_10': 0,
                                    'OFFAIR_UNLOCK': 0,
                                    'offair-10x-pts-multi': 0,
                                    'offair-unlock': 0},
                                'waitTimeMs': 0},
                    'shows': [{
                        'currency': 'USD',
                        'display': {
                            'accentColor': '#FFFFFF',
                            'bgImage': 'https://cdn.prod.hype.space/static/channel/TRIVIA/Trivia-frame.png',
                            'bgVideo': 'https://cdn.prod.hype.space/static/channel/TRIVIA/HQ-Trivia-portrait-70percentSpeed-190kbps-HVEC_H265.mp4',
                            'description': 'Are you a sponge of random facts? HQ '
                                           'Trivia is the viral hit live mobile '
                                           'game show where your trivia smarts '
                                           'helps you win real cash. Answer '
                                           'questions that range from easy to '
                                           'hard, and if you get them all right, '
                                           'you win or split the cash prize.',
                            'image': 'https://cdn.prod.hype.space/static/channel/TRIVIA/Trivia@3x.png?v=3',
                            'logo': 'https://cdn.prod.hype.space/static/channel/TRIVIA/Trivia@3x.png?v=3',
                            'subtitle': '$1,500 Prize!',
                            'summary': 'Answer trivia for cash prizes',
                            'title': 'HQ Trivia'},
                        'gameType': 'trivia',
                        'media': [],
                        'opt': 'hq-general',
                        'prizeCents': 150000,
                        'showId': 15077,
                        'showType': 'hq',
                        'startTime': '2022-04-01T01:00:00.000Z',
                        'vertical': 'general'}]}
        """
        return await self.fetch("GET", 'shows/schedule')

    async def easter_egg(self, type: str = "makeItRain"):
        """
        Get an extra life instant. Only one life in a month.
        response_data = {'data': True}
        """
        return await self.fetch("POST", "easter-eggs/{}".format(type))

    async def make_payout(self, email: str):
        """
        Withdraw your winnings to paypal email.
        response_data = {'data': {'amount': '$0.85',
                                  'created': '2020-11-25T06:40:01.726Z',
                                  'currency': 'USD',
                                  'metadata': {'client': 'Android/1.39.0',
                                               'ipAddress': '18.220.124.243',
                                               'payoutsConnected': True},
                                  'modified': '2020-11-25T06:40:01.726Z',
                                  'payoutId': 4651233,
                                  'status': 2,
                                  'targetEmail': 'sksakilahammed646@gmail.com',
                                  'targetPhone': None,
                                  'targetUserId': None,
                                  'userId': 26968460}}
        """
        return await self.fetch("POST", "users/me/payouts", {"email": email})

    async def send_code(self, phone: str, method: str = "sms"):
        """
        For registration send a sms verification code.
        response_data = {
                'callsEnabled': True,
                'expires': '2022-07-17T17:16:52.862Z',
                'phone': '+13152893528',
                'retrySeconds': 20,
                'verificationId': '39f36254-7d4e-43db-a92d-c9442fa88b5d'
            }
        """
        return await self.fetch("POST", "verifications", {"phone": phone, "method": method})

    async def confirm_code(self, verificationid: str, code: int):
        """
        Confirm the verification code from HQ.
        """
        return await self.fetch("POST", "verifications/{}".format(verificationid), {"code": code})

    async def register(self, verificationid: str, name: str, referral: str = None):
        """
        Registered an account.
        """
        return await self.fetch("POST", "users", {
            "country": "MQ==", "language": "eu",
            "referringUsername": referral,
            "username": name,
            "verificationId": verificationid})

    async def delete_avatar(self):
        """
        Delete your HQ avatar.
        response_data = {
                'avatarUrl': 'https://prd-bucket-hqtrivia-01012022.nyc3.cdn.digitaloceanspaces.com/da/purple.png',
                'created': '2020-12-23T16:22:47.000Z',
                'userId': 27196173,
                'username': 'bernita44'
            }
        """
        return await self.fetch("DELETE", "users/me/avatarUrl")

    async def add_referral(self, referral: str):
        """
        Add a referral to your account.
        response_data = {
                'avatarUrl': 'https://prd-bucket-hqtrivia-01012022.nyc3.cdn.digitaloceanspaces.com/da/purple.png',
                'created': '2020-12-23T16:22:47.000Z',
                'userId': 27196173,
                'username': 'bernita44'
            }
        """
        return await self.fetch("PATCH", "users/me", {"referringUsername": referral})

    async def add_friend(self, id: str):
        """
        Add a friend to your account.
        response_data = {
                'requestedUser': {
                    'avatarUrl': 'https://prd-bucket-hqtrivia-01012022.nyc3.cdn.digitaloceanspaces.com/da/gold.png',
                    'created': '2020-12-23T16:22:00.000Z',
                    'userId': 27196172,
                    'username': 'ntzamos'},
                'requestingUser': {
                    'avatarUrl': 'https://prd-bucket-hqtrivia-01012022.nyc3.cdn.digitaloceanspaces.com/da/purple.png',
                    'created': '2020-12-23T16:22:47.000Z',
                    'userId': 27196173,
                    'username': 'bernita44'},
                'status': 'PENDING'}
        """
        return await self.fetch("POST", "friends/{}/requests".format(id))

    async def friend_status(self, id: str):
        """
        Check status of your friend.
        response_data = {'status': None} # OUTBOUND_REQUEST, INBOUND_REQUEST, FRIENDS
        """
        return await self.fetch("GET", "friends/{}/status".format(id))

    async def remove_friend(self, id: str):
        """
        Remove a friend from your account.
        response_data = {'result': True}
        """
        return await self.fetch("DELETE", "friends/{}".format(id))

    async def accept_friend(self, id: str):
        """
        Accept a incoming friend request.
        response_data = {
                'requestedUser': {
                    'avatarUrl': 'https://prd-bucket-hqtrivia-01012022.nyc3.cdn.digitaloceanspaces.com/da/gold.png',
                    'created': '2020-12-23T16:22:00.000Z',
                    'userId': 27196172,
                    'username': 'ntzamos'},
                'requestingUser': {
                    'avatarUrl': 'https://prd-bucket-hqtrivia-01012022.nyc3.cdn.digitaloceanspaces.com/da/purple.png',
                    'created': '2020-12-23T16:22:47.000Z',
                    'userId': 27196173,
                    'username': 'bernita44'},
                'status': 'ACCEPTED'}
        """
        return await self.fetch("PUT", "friends/{}/status".format(id), {"status": "ACCEPTED"})

    async def friend_list(self):
        """
        Get your HQ friends list.
        """
        return await self.fetch("GET", "friends")

    async def check_username(self, name: str):
        """
        Check a username is available or not.
        response_data = {}
        """
        return await self.fetch("POST", "usernames/available", {"username": name})

    async def get_tokens(self, login_token: str):
        """
        Get access token of your HQ account.
        response_data = {
                'accessToken': 'eyJhbGciOiJI...',
                'admin': False,
                'authToken': 'eyJhbGciOiJIU...', # access token and auth token are totally different.
                'avatarUrl': 'https://prd-bucket-hqtrivia-01012022.nyc3.cdn.digitaloceanspaces.com/da/purple.png',
                'canEnterReferral': True,
                'guest': False,
                'loginToken': 'KwmTCpQzIqiLL...dEXRcSeGk',
                'tester': False,
                'userId': 27196173,
                'username': 'bernita44',
                'wasReferralDenied': False
            }
        """
        return await self.fetch("POST", "tokens", {'token': login_token})

    async def edit_username(self, username: str):
        """
        Edit your username in HQ Trivia.
        response_data = {
                    'avatarUrl': 'https://prd-bucket-hqtrivia-01012022.nyc3.cdn.digitaloceanspaces.com/da/purple.png',
                    'created': '2020-12-23T16:22:47.000Z',
                    'userId': 27196173,
                    'username': 'bernita44'
                }
        """
        return await self.fetch("PATCH", "users/me", {"username": username})

    async def get_login_token(self):
        """
        Get your HQ Trivia account login token.
        response_data = {
                'loginToken': 'KwmTCX.....XRcSeGk'
            }
        """
        return await self.fetch("GET", "users/me/token")

    async def send_documents(self, id, email, paypal_email, country):
        return await self.fetch("POST", "users/{}/payouts/documents".format(id),
                          {"email": email, "country": country, "payout": paypal_email})

    async def register_device_token(self, token):
        return await self.fetch("POST", "users/me/devices", {"token": token})

    async def config(self):
        """
        Get extra details of your HQ account.
        response_data = {
                'achievements': {'lobbyEnabled': True},
                'bandwidthCheck': 'https://prd-bucket-hqtrivia-01012022.nyc3.cdn.digitaloceanspaces.com/static/bird.jpg',
                'batchSize': 50,
                'betaUnlockEnabled': True,
                'blueMercuryEnabled': False,
                'buyBackInOverlay': {'noAnswerDurationMs': 10000,
                                     'wrongAnswerDurationMs': 10000},
                'captchaUrl': 'https://www.hqtrivia.com/verify',
                'cashReferrals': False,
                'changeAnswer': True,
                'ddStatsEnabled': False,
                'dynamicPotClient': False,
                'easterEggs': {'makeItRain': {'enabled': True, 'interval': 2592000}},
                'elPromptMs': 5000,
                'erase1Cost': 2,
                'erase1Enabled': True,
                'friends': {
                         'answerSharingEnabled': True,
                         'incomingRequestPollIntervalMs': 60000,
                         'maxAnswerSharingQuestions': 1000,
                         'maxFriendAnswersPerQuestion': 5,
                         'maxFriendsAnswersPerChoice': 1000,
                         'minAndroidVersion': 'Android/1.6.1',
                         'minIOsBetaVersion': 'iOS-Beta/1.0.0 b1',
                         'minIOsDevVersion': 'iOS-Dev/1.0.0 b1',
                         'minIOsVersion': 'iOS/1.2.9 b1',
                         'nearbyEnabled': True,
                         'resultSharingEnabled': True,
                         'statusSharingEnabled': True
                     },
                'hqUniversityAction': '',
                'iapFlags': {
                      'ingameBuyBack': True,
                      'ingameBuyBackWords': True,
                      'ingameNextGame': False,
                      'prerollTooltip': False
                    },
                'inGameBlueMercury': False,
                'inGameIapToolTip': {'durationMs': 10000, 'times': 1000},
                'keepPlaying': False,
                'maxErase1s': 8,
                'minVersion': {'android': '1.41.0', 'ios': '1.5.12'},
                'mpt': 4,
                'multimedia': {
                        'duckSecs': 4,
                        'enabled': True,
                        'sfxVolumes': {'audio': 0, 'image': 1, 'video': 0.25}
                    },
                'multipeerEnabled': False,
                'newLobby': False,
                'newPushFlow': False,
                'newUserSportsOptIn': False,
                'nonce': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjI3MTk2MTczLCJpYXQiOjE2NTgwNzg4NDQsImV4cCI6MTY1ODA3OTE0NCwiaXNzIjoiaHlwZXF1aXovMSJ9.r8j2kHix_OS9QwhVppy-JeQX8ZiSK97x1lC6WVQugbE',
                'offairTriviaApplovinNetworkEnabled': False,
                'offairTriviaTelemetryLogsEnabled': False,
                'oneSignalEnabled': True,
                'payouts': {'active': True, 'mode': 'live', 'threshold': '$5'},
                'popularChoice': False,
                'productPlacements': {'adminCalloutModal': [{'productId': 'com.intermedia.hq.iap.extralife.1',
                                                             'quantity': 1},
                                                            {'productId': 'com.intermedia.hq.iap.extralife.3',
                                                             'quantity': 3}],
                                      'adminMultiplierCalloutModal': [{'productId': 'com.intermedia.hq.iap.pointmultiplier.5X',
                                                                      'quantity': 1},
                                                                     {'productId': 'com.intermedia.hq.iap.pointmultiplier.10X',
                                                                      'quantity': 1},
                                                                     {'productId': 'com.intermedia.hq.iap.pointmultiplier.15X',
                                                                      'quantity': 1}],
                                      'extraLivesInfo': [{'productId': 'com.intermedia.hq.iap.extralife.1',
                                                          'quantity': 1},
                                                         {'productId': 'com.intermedia.hq.iap.extralife.3',
                                                          'quantity': 3}],
                                      'extraLivesModal': [{'productId': 'com.intermedia.hq.iap.extralife.1',
                                                           'quantity': 1},
                                                          {'productId': 'com.intermedia.hq.iap.extralife.3',
                                                           'quantity': 3}],
                                      'hqProModal': [],
                                      'ingameBuyBack': [{'productId': 'com.intermedia.hq.iap.extralife.1',
                                                         'quantity': 1}],
                                      'ingameNextGame': [{'productId': 'com.intermedia.hq.iap.extralife.1',
                                                          'quantity': 1}],
                                      'prerollTooltip': [{'productId': 'com.intermedia.hq.iap.extralife.1',
                                                          'quantity': 1}]}, 'recommendedVersion': {'android': '1.41.0', 'ios': '1.5.3'},
                'redEnigma': True,
                'sampleRate': 1,
                'settings': True,
                'showReferrals': False,
                'storeEnabled': True,
                'storeIAPEnabled': False,
                'streamConfiguration': {'allowsMultipleStreams': False,
                                        'allowsReconnect': True,
                                        'android': {'maxDeviation': 80,
                                                    'maxStepUps': 5,
                                                    'minimumMillisecondsBufferToStart': 1000,
                                                    'optimalMillisecondsFromLiveEdge': 1000},
                                        'downStepFloor': 1,
                                        'downStepSampleSize': 10,
                                        'hlsEnabled': True,
                                        'ios': {'hlsEnabled': True},
                                        'isDownStepEnabled': True,
                                        'isUpStepEnabled': True,
                                        'upStepCeil': 25,
                                        'upStepSampleSize': 60},
                'superWheelEnabled': True,
                'tags': {'cdnCanary': 'false'},
                'telemetry': {'batchSize': 50,
                              'enabled': False,
                              'host': 'https://telemetry.prod.hype.space'}, 'watchdogEnabled': True,
                'wave': {'outOfGameEnabled': True},
                'webStoreUrl': 'https://store.prod.hype.space/products'}
        """
        return await self.fetch("GET", "config")

    async def get_optins(self):
        return await self.fetch("GET", "opt-in")

    async def set_optin(self, name: str, value: bool):
        return await self.fetch("POST", "opt-in", {"value": value, "opt": name})

    async def season_xp(self):
        return await self.fetch("GET", "seasonXp/settings")

    async def referrals(self):
        return await self.fetch("GET", "show-referrals")

    async def facebook_login(self, access_token):
        return await self.fetch("POST", "users/provider-auth", {"type":"FACEBOOK","token": access_token})

    async def google_login(self, jwt_token):
        return await self.fetch("POST", "users/provider-auth", {"type":"GOOGLE","token": jwt_token})

    async def swipe(self):
        """
        Swipe HQ account and earn an extra life.
        response_data = {'data': True}
        """
        return await self.fetch("POST", "easter-eggs/makeItRain")

    async def purchase_life(self, amount: int):
        response_data = {
                    'coinsPurchased': 0,
                    'coinsTotal': 24562,
                    'itemsPurchased': {'extra-life': 1},
                    'itemsTotal': {'extra-life': 2, 'super-spin': 2},
                    'subscriptions': [],
                    'transactionId': None
                }
        return await self.fetch("POST", "store/com.intermedia.hq.item.extralife.{}x/purchase".format(amount))

    async def purchase_eraser(self, amount: int):
        response_data = {
                    'coinsPurchased': 0,
                    'coinsTotal': 24462,
                    'itemsPurchased': {'eraser': 1},
                    'itemsTotal': {'eraser': 1, 'extra-life': 2, 'super-spin': 2},
                    'subscriptions': [],
                    'transactionId': None
                }
        return await self.fetch("POST", "store/com.intermedia.hq.item.erasers.{}x/purchase".format(amount))

    async def purchase_super_spin(self, amount: int):
        response_data = {
                    'coinsPurchased': 0,
                    'coinsTotal': 24312,
                    'itemsPurchased': {'super-spin': 1},
                    'itemsTotal': {'eraser': 1, 'extra-life': 2, 'super-spin': 3},
                    'subscriptions': [],
                    'transactionId': None
                }
        return await self.fetch("POST", "store/com.intermedia.hq.item.superspin.{}x/purchase".format(amount))

    async def leaderboard(self, mode: str):
        """
        Get weekly and alltime leaderboard.
        response_data = {
                    'data': [
                        {
                            'avatarUrl': 'https://prd-bucket-hqtrivia-01012022.nyc3.cdn.digitaloceanspaces.com/a/07/45653-5HZUxw.jpg',
                            'total': '$100,096',
                            'totalCents': 10009639,
                            'userId': 45653,
                            'username': 'brillipz',
                            'wins': 27
                        },
                        {
                            'avatarUrl': 'https://prd-bucket-hqtrivia-01012022.nyc3.cdn.digitaloceanspaces.com/da/gold.png',
                            'total': '$100,003',
                            'totalCents': 10000256,
                            'userId': 5433625,
                            'username': 'magdaddy17',
                            'wins': 2
                        }
                    ]}
        """
        return await self.fetch("GET", "users/leaderboard?mode={}".format(mode))

    async def set_avatar(self, file: str):
        return await self.fetch("POST", "users/me/avatar", files={"file": ("file", open(file, 'rb').read(), 'image/jpeg')})

    async def store(self):
        return await self.fetch("GET", "store/products")

    async def start_offair(self):
        return await self.fetch('POST', "offair-trivia/start-game")

    async def offair_trivia(self, id: str):
        return await self.fetch('GET', 'offair-trivia/{}'.format(id))

    async def send_offair_answer(self, id: str, answer_id: str):
        return await self.fetch('POST', 'offair-trivia/{}/answers'.format(id), {"offairAnswerId": answer_id})

    async def custom(self, method, func, data):
        return await self.fetch(method, func, data)


class HQApi(BaseHQApi):
    def __init__(self, token: str = None, login_token: str = None,
                 version: str = "1.50.0", host: str = "https://api-quiz.hype.space/",
                 proxy: str = None, verify: bool = True):
        super().__init__(token, login_token)
        self.version = "2.4.3"
        self.token = token
        self.login_token = login_token
        self.hq_version = version
        self.host = host
        self.v = verify
        self.p = dict(http=proxy, https=proxy)
        self.headers = {
            # "x-hq-client": "Android/" + self.hq_version
            "x-hq-client": "iPhone8,2"
        }
        if login_token:
            self.token = asyncio.run(self.get_tokens(login_token))["accessToken"]
        if self.token:
            self.headers["Authorization"] = "Bearer " + self.token

    async def fetch(self, method = "GET", func = "", data = None, files = None):
        if data is None: data = {}
        async with aiohttp.ClientSession() as session:
            try:
                response = await session.request(method, self.host + "{}".format(func), headers = self.headers, data = data)
                content = await response.json()
                error = content.get("error")
                if error:
                    raise ApiResponseError(error)
                return content
            except json.decoder.JSONDecodeError:
                raise BannedIPError("Your IP is banned")

    async def decode_jwt(self, jwt_text: str):
        return jwt.decode(jwt_text.encode(), verify=False)

    async def set_token(self, token):
        self.token = token
        if self.token:
            self.headers["Authorization"] = "Bearer " + self.token

    def __str__(self):
        return "<HQApi {} token={}>".format(self.version, self.token)
