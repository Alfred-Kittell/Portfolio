using System;
using System.Text;

namespace RtspClientSharp.Rtsp
{
    /// <summary>
    /// Сообщение запроса RTSP
    /// </summary>
    class RtspRequestMessage : RtspMessage
    {
        private readonly Func<uint> _cSeqProvider;

        /// <summary>
        /// Метод протокола RTSP
        /// </summary>
        public RtspMethod Method { get; }
        /// <summary>
        /// Адрес хоста
        /// </summary>
        public Uri ConnectionUri { get; }
        /// <summary>
        /// Имя приложения
        /// </summary>
        public string UserAgent { get; }


        /// <summary>
        /// Конструктор запроса
        /// </summary>
        /// <param name="method">Метод протокола RTSP</param>
        /// <param name="connectionUri">Адрес хоста</param>
        /// <param name="protocolVersion">Версия протокола</param>
        /// <param name="cSeqProvider">Порядковый номер сообщения</param>
        /// <param name="userAgent">Имя приложения</param>
        /// <param name="session">Сессия</param>
        public RtspRequestMessage(RtspMethod method, Uri connectionUri, Version protocolVersion, Func<uint> cSeqProvider, string userAgent, string session) : base(cSeqProvider(), protocolVersion)
        {
            Method = method;
            ConnectionUri = connectionUri;
            _cSeqProvider = cSeqProvider;
            UserAgent = userAgent;

            if (!string.IsNullOrEmpty(session))
                Headers.Add("Session", session);
        }

        /// <summary>
        /// Обновление номера запроса
        /// </summary>
        public void UpdateSequenceNumber()
        {
            CSeq = _cSeqProvider();
        }

        /// <summary>
        /// Представление запроса в виде строки
        /// </summary>
        /// <returns>Текст запроса</returns>
        public override string ToString()
        {
            var queryBuilder = new StringBuilder(512);

            queryBuilder.AppendFormat("{0} {1} RTSP/{2}\r\n", Method, ConnectionUri, ProtocolVersion.ToString(2));
            queryBuilder.AppendFormat("CSeq: {0}\r\n", CSeq);

            if (!string.IsNullOrEmpty(UserAgent))
                queryBuilder.AppendFormat("User-Agent: {0}\r\n", UserAgent);

            foreach (string headerName in Headers.AllKeys)
                queryBuilder.AppendFormat("{0}: {1}\r\n", headerName, Headers[headerName]);

            queryBuilder.Append("\r\n");

            return queryBuilder.ToString();
        }
    }
}