"""
Автоматическая настройка платы прибора

(С) 2023 БО-Энерго, Альфред Дж. Киттелл
"""

# -- INNER --
from bo_chrone.chroneControl import ChroneControl

###########################################################


def main():
    """ """
    ip = "10.1.3.14"
    #ip = "192.168.0.1"
    port = 1024
    chrone = ChroneControl(ip, port)

    p = [
        [8, 3],
        [9, 7],
        [32, 10],
        [33, 1],
        [34, 3],
        [35, 14],
        [52, 112],
        [53, 23],
        [54, 0],
        [55, 0],
        [56, 0],
        [57, 0],
        [58, 0],
    ]

    try:
        chrone.connect()
        print(f"All parameters:")
        for item in p:
            before = chrone.getValue(item[0])
            if before != item[1]:
                chrone.setValue(item[0], item[1])
            after = chrone.getValue(item[0])
            print(f"\t{item[0]} - before: {before}\tafter: {after}")

    except Exception as ex:
        print(f"Error! {ex}")


if __name__ == '__main__':
    main()
