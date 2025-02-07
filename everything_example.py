from everything import *


def main() -> None:
    print("`math', `multiprocessing.dummy.connection' and `np' were never imported?!")

    print(f"math.pi={math.pi}")
    print(
        "multiprocessing.dummy.connection.Connection=",
        multiprocessing.dummy.connection.Connection,
        sep="",
    )
    print(
        "np.fromfunction(lambda y, x: 2 * x + y, (5, 5), dtype=int)=",
        np.fromfunction(lambda y, x: 2 * x + y, (5, 5), dtype=int),
        sep="\n",
    )


if __name__ == "__main__":
    main()
