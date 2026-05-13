using System;

namespace RtspClientSharp.Rtsp
{
    /// <summary>
    /// Фабрика запросов к хосту по протоколу RTSP
    /// </summary>
    class RtspRequestMessageFactory
    {
        private static readonly Version ProtocolVersion = new Version(1, 0);

        private uint _cSeq;
        private readonly Uri _rtspUri;
        private readonly string _userAgent;

        /// <summary>
        /// 
        /// </summary>
        public Uri ContentBase { get; set; }
        /// <summary>
        /// Сессия
        /// </summary>
        public string SessionId { get; set; }


        /// <summary>
        /// Конструктор фабрики запросов
        /// </summary>
        /// <param name="rtspUri">Адрес хоста</param>
        /// <param name="userAgent">Имя приложения</param>
        public RtspRequestMessageFactory(Uri rtspUri, string userAgent)
        {
            _rtspUri = rtspUri ?? throw new ArgumentNullException(nameof(rtspUri));
            _userAgent = userAgent;
        }

        /// <summary>
        /// Создание запроса на поддерживаемые методы
        /// </summary>
        /// <returns>Запрос</returns>
        public RtspRequestMessage CreateOptionsRequest()
        {
            var rtspRequestMessage = new RtspRequestMessage(RtspMethod.OPTIONS, _rtspUri, ProtocolVersion, NextCSeqProvider, _userAgent, SessionId);
            return rtspRequestMessage;
        }

        /// <summary>
        /// Создание запроса на описание содержимого
        /// </summary>
        /// <returns>Запрос</returns>
        public RtspRequestMessage CreateDescribeRequest()
        {
            var rtspRequestMessage = new RtspRequestMessage(RtspMethod.DESCRIBE, _rtspUri, ProtocolVersion, NextCSeqProvider, _userAgent, SessionId);
            rtspRequestMessage.Headers.Add("Accept", "application/sdp");
            return rtspRequestMessage;
        }

        /// <summary>
        /// Создание запроса на транспортный протокол RTP/AVP/TCP
        /// </summary>
        /// <param name="trackName">Имя трека</param>
        /// <param name="rtpChannel">RTP канал</param>
        /// <param name="rtcpChannel">RTCP канал</param>
        /// <returns>Запрос</returns>
        public RtspRequestMessage CreateSetupTcpInterleavedRequest(string trackName, int rtpChannel, int rtcpChannel)
        {
            Uri trackUri = GetTrackUri(trackName);

            var rtspRequestMessage = new RtspRequestMessage(RtspMethod.SETUP, trackUri, ProtocolVersion, NextCSeqProvider, _userAgent, SessionId);
            rtspRequestMessage.Headers.Add("Transport", $"RTP/AVP/TCP;unicast;interleaved={rtpChannel}-{rtcpChannel}");
            return rtspRequestMessage;
        }

        /// <summary>
        /// Создание запроса на транспортный протокол RTP/AVP/UDP
        /// </summary>
        /// <param name="trackName">Имя трека</param>
        /// <param name="rtpPort">RTP порт</param>
        /// <param name="rtcpPort">RTCP порт</param>
        /// <returns>Запрос</returns>
        public RtspRequestMessage CreateSetupUdpUnicastRequest(string trackName, int rtpPort, int rtcpPort)
        {
            Uri trackUri = GetTrackUri(trackName);

            var rtspRequestMessage = new RtspRequestMessage(RtspMethod.SETUP, trackUri, ProtocolVersion, NextCSeqProvider, _userAgent, SessionId);
            rtspRequestMessage.Headers.Add("Transport", $"RTP/AVP/UDP;unicast;client_port={rtpPort}-{rtcpPort}");
            return rtspRequestMessage;
        }

        /// <summary>
        /// Создание запроса на начало вещание
        /// </summary>
        /// <returns>Запрос</returns>
        public RtspRequestMessage CreatePlayRequest()
        {
            Uri uri = GetContentBasedUri();

            var rtspRequestMessage = new RtspRequestMessage(RtspMethod.PLAY, uri, ProtocolVersion, NextCSeqProvider, _userAgent, SessionId);
            rtspRequestMessage.Headers.Add("Range", "npt=0.000-");
            return rtspRequestMessage;
        }

        /// <summary>
        /// Создание запроса остановки вещания
        /// </summary>
        /// <returns>Запрос</returns>
        public RtspRequestMessage CreateTeardownRequest()
        {
            var rtspRequestMessage = new RtspRequestMessage(RtspMethod.TEARDOWN, _rtspUri, ProtocolVersion,
                NextCSeqProvider, _userAgent, SessionId);
            return rtspRequestMessage;
        }

        /// <summary>
        /// Создание запроса на получение параметров
        /// </summary>
        /// <returns>Запрос</returns>
        public RtspRequestMessage CreateGetParameterRequest()
        {
            var rtspRequestMessage = new RtspRequestMessage(RtspMethod.GET_PARAMETER, _rtspUri, ProtocolVersion, NextCSeqProvider, _userAgent, SessionId);
            return rtspRequestMessage;
        }

        private Uri GetContentBasedUri()
        {
            if (ContentBase != null)
                return ContentBase;

            return _rtspUri;
        }

        /// <summary>
        /// Увеличить и вернуть номер запроса
        /// </summary>
        /// <returns>Следующий номер запроса</returns>
        private uint NextCSeqProvider()
        {
            return ++_cSeq;
        }

        /// <summary>
        /// Объединение адреса хоста и имени трека
        /// </summary>
        /// <param name="trackName">Имя трека</param>
        /// <returns>Полный адрес трека</returns>
        private Uri GetTrackUri(string trackName)
        {
            Uri trackUri;

            if (!Uri.IsWellFormedUriString(trackName, UriKind.Absolute))
            {
                var uriBuilder = new UriBuilder(GetContentBasedUri());

                trackName = trackName ?? "";

                bool trackNameStartsWithSlash = trackName.StartsWith("/");

                if (uriBuilder.Path.EndsWith("/"))
                    uriBuilder.Path += trackNameStartsWithSlash ? trackName.Substring(1) : trackName;
                else
                    uriBuilder.Path += trackNameStartsWithSlash ? trackName : "/" + trackName;

                trackUri = uriBuilder.Uri;
            }
            else
                trackUri = new Uri(trackName, UriKind.Absolute);

            return trackUri;
        }
    }
}