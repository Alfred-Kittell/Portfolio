using System;
using System.Runtime.Serialization;

namespace RtspClientSharp.Rtsp
{
    [Serializable]
    public class RtspClientException : Exception
    {
        public RtspClientException() { }

        public RtspClientException(string message) : base(message) { }

        public RtspClientException(string message, Exception inner) : base(message, inner) { }

        protected RtspClientException(SerializationInfo info, StreamingContext context) : base(info, context) { }
    }

    [Serializable]
    public class RtspParseResponseException : RtspClientException
    {
        public RtspParseResponseException(string message) : base(message) { }

    }

    [Serializable]
    public class RtspBadResponseException : RtspClientException
    {
        public RtspBadResponseException(string message) : base(message) { }
    }

    [Serializable]
    public class RtspBadResponseCodeException : RtspClientException
    {
        public RtspStatusCode Code { get; }

        public RtspBadResponseCodeException(RtspStatusCode code) : base($"Bad response code: {code}")
        {
            Code = code;
        }
    }
}