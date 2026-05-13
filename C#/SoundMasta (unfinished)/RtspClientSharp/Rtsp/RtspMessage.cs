using System;
using System.Collections.Specialized;

namespace RtspClientSharp.Rtsp
{
    /// <summary>
    /// Базовый класс сообщений RTSP
    /// </summary>
    abstract class RtspMessage
    {
        /// <summary>
        /// Порядковый номер запроса
        /// </summary>
        public uint CSeq { get; protected set; }
        /// <summary>
        /// Версия протокола
        /// </summary>
        public Version ProtocolVersion { get; }
        /// <summary>
        /// Заголовки запроса
        /// </summary>
        public NameValueCollection Headers { get; }


        /// <summary>
        /// Базовый конструктор запроса
        /// </summary>
        /// <param name="cSeq">Порядковый номер запроса</param>
        /// <param name="protocolVersion">Версия протокола</param>
        protected RtspMessage(uint cSeq, Version protocolVersion)
        {
            CSeq = cSeq;
            ProtocolVersion = protocolVersion;
            Headers = new NameValueCollection();
        }

        /// <summary>
        /// Базовый конструктор ответа
        /// </summary>
        /// <param name="cSeq">Порядковый номер запроса</param>
        /// <param name="protocolVersion">Версия протокола</param>
        /// <param name="headers">Заголовки запроса</param>
        protected RtspMessage(uint cSeq, Version protocolVersion, NameValueCollection headers)
        {
            CSeq = cSeq;
            ProtocolVersion = protocolVersion;
            Headers = headers;
        }
    }
}