

namespace RtspClientSharp.Rtsp
{
    /// <summary>
    /// Методы протокола RTSP
    /// </summary>
    enum RtspMethod
    {
        /// <summary>
        /// Запрос описания содержимого
        /// </summary>
        DESCRIBE,
        /// <summary>
        /// Запрос поддерживаемых методов
        /// </summary>
        OPTIONS,
        /// <summary>
        /// Запрос установки транспортного механизма для содержимого
        /// </summary>
        SETUP,
        /// <summary>
        /// Запрос начала вещания содержимого
        /// </summary>
        PLAY,
        /// <summary>
        /// Запрос временной остановки вещания
        /// </summary>
        PAUSE,
        /// <summary>
        /// Запрос на записывание содержимого сервером
        /// </summary>
        RECORD,
        /// <summary>
        /// Перенаправление на другое содержимое
        /// </summary>
        REDIRECT,
        /// <summary>
        /// Обновление данных описания содержимого
        /// </summary>
        ANNOUNCE,
        /// <summary>
        /// Запрос указанных параметров у сервера
        /// </summary>
        GET_PARAMETER,
        /// <summary>
        /// Установка параметров сервера
        /// </summary>
        SET_PARAMETER,
        /// <summary>
        /// Информирования клиента об асинхронном событии для сеанса в состоянии воспроизведениявв
        /// </summary>
        PLAY_NOTIFY,
        /// <summary>
        /// Запрос остановки вещания
        /// </summary>
        TEARDOWN
    }
}