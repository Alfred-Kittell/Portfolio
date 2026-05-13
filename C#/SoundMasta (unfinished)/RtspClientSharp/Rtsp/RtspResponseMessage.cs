using System;
using System.Collections.Specialized;
using System.Diagnostics;
using System.IO;
using System.Text;

namespace RtspClientSharp.Rtsp
{
    /// <summary>
    /// Сообщение ответа RTSP
    /// </summary>
    class RtspResponseMessage : RtspMessage
    {
        private static readonly ArraySegment<byte> EmptySegment = new ArraySegment<byte>(Array.Empty<byte>(), 0, 0);


        /// <summary>
        /// Код ответа
        /// </summary>
        public RtspStatusCode StatusCode { get; }

        /// <summary>
        /// Тело ответа
        /// </summary>
        public ArraySegment<byte> ResponseBody { get; set; } = EmptySegment;

        /// <summary>
        /// Конструктор ответа
        /// </summary>
        /// <param name="statusCode">Код ответа</param>
        /// <param name="protocolVersion">Версия протокола</param>
        /// <param name="cSeq">Порядковый номер сообщения</param>
        /// <param name="headers">Заголовки ответа</param>
        public RtspResponseMessage(RtspStatusCode statusCode, Version protocolVersion, uint cSeq, NameValueCollection headers) : base(cSeq, protocolVersion, headers)
        {
            StatusCode = statusCode;
        }

        /// <summary>
        /// Парсер ответа
        /// </summary>
        /// <param name="byteSegment">Данные</param>
        /// <returns>Ответ</returns>
        public static RtspResponseMessage Parse(ArraySegment<byte> byteSegment)
        {
            Debug.Assert(byteSegment.Array != null, "byteSegment.Array != null");

            var headersStream = new MemoryStream(byteSegment.Array, byteSegment.Offset, byteSegment.Count, false);
            var headersReader = new StreamReader(headersStream);

            string startLine = headersReader.ReadLine();

            if (startLine == null)
                throw new RtspParseResponseException("Empty response");

            string[] tokens = GetFirstLineTokens(startLine);

            Version protocolVersion = ParseProtocolVersion(tokens[0]);
            RtspStatusCode statusCode = ParseStatusCode(tokens[1]);

            NameValueCollection headers = HeadersParser.ParseHeaders(headersReader);

            uint cSeq = 0;
            string cseqValue = headers.Get("CSEQ");

            if (cseqValue != null)
                uint.TryParse(cseqValue, out cSeq);

            return new RtspResponseMessage(statusCode, protocolVersion, cSeq, headers);
        }

        /// <summary>
        /// Представление запроса в виде строки
        /// </summary>
        /// <returns>Текст ответа</returns>
        public override string ToString()
        {
            var sb = new StringBuilder();
            sb.AppendFormat("RTSP/{0} {1} {2}\r\nCSeq: {3}\r\n",
                ProtocolVersion, (int)StatusCode, StatusCode, CSeq);

            foreach (string key in Headers.AllKeys)
                sb.AppendFormat("{0}: {1}\r\n", key, Headers.Get(key));

            if (ResponseBody.Count != 0)
            {
                sb.AppendLine();

                string bodyString = Encoding.ASCII.GetString(ResponseBody.Array,
                    ResponseBody.Offset, ResponseBody.Count);

                sb.Append(bodyString);
            }

            return sb.ToString();
        }

        /// <summary>
        /// Парсер кода ответа
        /// </summary>
        /// <param name="statusCode">Строка с кодом</param>
        /// <returns>Код ответа</returns>
        private static RtspStatusCode ParseStatusCode(string statusCode)
        {
            if (!int.TryParse(statusCode, out int code))
                throw new RtspParseResponseException($"Invalid status code: {statusCode}");

            return (RtspStatusCode)code;
        }

        /// <summary>
        /// Парсер первой строки ответа
        /// </summary>
        /// <param name="startLine">Строка ответа</param>
        /// <returns>Токены первой строки</returns>
        private static string[] GetFirstLineTokens(string startLine)
        {
            string[] tokens = startLine.Split(' ');

            if (tokens.Length == 0)
                throw new RtspParseResponseException("Missing method");
            if (tokens.Length == 1)
                throw new RtspParseResponseException("Missing URI");
            if (tokens.Length == 2)
                throw new RtspParseResponseException("Missing protocol version");

            return tokens;
        }

        /// <summary>
        /// Парсер протокола
        /// </summary>
        /// <param name="protocolNameVersion">Строка с протоколом</param>
        /// <returns>Версия протокола</returns>
        private static Version ParseProtocolVersion(string protocolNameVersion)
        {
            int slashPos = protocolNameVersion.IndexOf('/');

            if (slashPos == -1)
                throw new RtspParseResponseException($"Invalid protocol name/version format: {protocolNameVersion}");

            string version = protocolNameVersion.Substring(slashPos + 1);
            if (!Version.TryParse(version, out Version protocolVersion))
                throw new RtspParseResponseException($"Invalid RTSP protocol version: {version}");

            return protocolVersion;
        }
    }
}