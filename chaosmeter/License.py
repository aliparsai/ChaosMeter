#! /usr/bin/env python3

import base64
import bz2


def returnLicense():
    """

    :return:
    :rtype:
    """
    licenseText = b'QlpoOTFBWSZTWYSRie8AAjT/gEBQaEBQ5//9P///4H////BgOH0NSz7UrQHHs1L1rrEVAoAUJIUgEgHkPe86SD1x7L7W9abvs92z1fTdmHvmPKq9gBX1z74PRQHbnPve7fbz08u+6vilfbPrNm2o21764PeiWWlt99zd3vKErqyk2sMkbGtSwALZatWR999EF17vu97tt3ihe10LYa3nO2y2yuejBpoIAgmhNAmk2k0apvSaDFB6mynqep6nqYIA0yAhCIQk1E9Rp6AAQGAQBiAaYSmQiIyqflT9Em1BoAADQ0PUA9QANDQJNJIQE1MjJHpJD9UGNQ0NDQPU0ADQAESSZAQCU2TQKbUyJp7UyjTIaGIA9TQAJNRECTEMKTU1PUfqnlPap6jeqZD1AHqAABkOJIQ8vd/E2P6kWKn56AoBP90gf2IQ/ER/1L+o/noP/cVRLD8/5/piVAmaUwhdPEppl/92/pARabbbf81eN1nBL3xPL+y8mrSTaNncj9xAACcsfVefXhsjAj9/55xrIRyhpEfj/pqiXj7PxmOwv43rjy161+79Z9Occ/7qPN5Du30TaXSU7eUMRQQKB0k1i1GEvKIWUnov9YX0NWA3wv3KHK3cayHH/7FgMdL0pvXNhziBwX1XvSLf4i2k4orrnX62134trSVpaKKTvcEV2zvdwMKJSFwuV7tPYPBTjY/8q3AvfQ1QobOv2cnl+B6n0V4LsdXx27jtxM27jeld5GdVj8oLLn5Op+LXXUV9zbVb0WrjNtvlA3q9NI2eotmFdHTDqonT4IAiAD3kkh90RSB+4WyKsEjUqsYKqixSIqrEVRWCRYigKoyRWKoIxRTxRX256PCH31RXb49tMeOmNsZ1O8pGc2ZY1TeaoTdkw8mKiDgs55wp47vFdbgoVFPQeBNXG3b6uvtkNL3svdMWFTvvRuMP24UHuv+T+4e8Ee78vnj8PonPx/L9N9SVQhO88+PGXa3pybokVRRuPjsq38U7IKJT37e5vKgyWITzPhnvOn06aVK/PeX5yoyh08d+3k+PnWB7gfRn4+NLgCx/dd2T9hFHF7+fRrgfNvybjdjzSOUgidSiBz6gaeJI73/DeyfluNdZ3uHz9fp+tPze6gMWIIMBYbpKIsigjbj58/Hy/HX1Pr5ePbqPPSdN1/wQiVKH2MfEbP+vpr5etKBvEi45fDTyNRJK51uAH+L5bn49UTog9xQAH93nrPsABnl10b5vbT2WFrdotX0v2jYIfMW3VEA9HHzrUcrx6OGHivZ4Vx4bbb1ieu3JkAHAKfEgAeWk59TyHMdGxSg0Uvprb6/QdtQOL2+h0CcFO/O3vWOnk45thfZ7IsK/Ira17VtxZnh2DoK4vKsDG4VhJkOSqkqCqvj0lkpM4QrIQ1MOjAucf3/bVzAOKCetWyMjWjGebyrabhoPl1c1Ax3eX5DSIIn8Igiumudbmq4fjlcjoLgEbmNS6IIj1N4Ijk2JQsoazVY7uJrPNdbYXyEH6OiH4RPWvF/LlyOvXa36i/XqvfimrUXD88o9xZRdwdx3bzljUK5UwjC+Vqw4q9blc3WVx9BnAEGAVd1bgoHicjJq6vxxGJrwvFekXgUi1hFXYzJqpBnZ7Fi7kFQbY5mTX9XP1wGoIBo35aXzsCiPZj4axkVkw8mfBvPBuTmsV8Fn5oZgrKNzadZrpWOVBXO8mUfHNH5qu2uFd+YgxG+yYsa9PQ8+KoYjKposQ7HBMahJQZyXFNfRzEP1pqtftVPjDhGmHDn2Vbx7Qd8BDbhM3BbZBs6AZS6zDYvblEmpmmHqonbbD1rNXVRzjfSwwU4KKiIiCKrBRXba6789cw9Nf32749dLz2067aiBocHdBUTal6WeQ1raIbEMN5XWQcakRjXC47knaaEi/ES4vB69Y59utHULVB/PT9kPY7YdCjMAtoKna43jVlIMimSJwvtpmVIOm6tYbytGtYwSMYkkG+XIkhChpjqdNdOGdvjOk30di2Km76FM1mxXMPgylaju4eYeUiHbo+95jM9o9jlCz10EXHr0E/jOgkghDl3ue27uFwdX13exAdAiuxpuSQtId42hOjwrI38yw/J/i20eYH3vTju3TpVFh5Yc1ffPW7TWnLaB4fT9zGjo3N8rmj+HeosHq8yUYmgn4uKxE3ClitVYaWNpB6CQPguraipcOZFN6KcNsxIVxnRVrpJ0L4XmVEdGZuk16LzMm5Ns+mNVi/ThjIbKhqVMq8piTcSf2pkCzp3Me/XEPl7fQG9oLEPUgDdhxWz396gtLooJ0FVyRlrxpozWnaYdxnsbtalzEMy7W6S3pQcQ4sE1U7KnmY/3Wql+g+ipp30N91IIUDZbUKPWZHN7+dURNw8mNuXHvQSa64Y/zte+R8RYLhBW7/9nD2Z6XQkgpeJH26EKNT78yHmazDqDb/MKyPuvW+o1SrZrIpGAab7+Rr7qRicgPyuLUDvBVyRlen+lGWYWqiYMEfNmeGkPt3Oa/Ft8d1LLRpxD6uv0d7tST3g0N+kiNpS69FlKHVdJnZq9lwxyubjGB0h6LoZ6aSK03nHLmrkWJ63NLOc8jghhJ9+vjrql6N79By1+/I8lgSkmbDgn1fetP7PqG9voe26aLz1UfMOISD+KxyahBeEg1orRYSIQ9abseYw+DPx1i6fKQoSuyRa2ZiNv0JW7ipqg9x8OPO+pseDp5gA+3c2qSl0HdQk8J4CHQvzrVqbMAk+11v0JOWAgQSiAizqruOnpdePKCGQwpWSCA5tVVlKrx/iKAxZJGj8UmiA7lBE+i55KII877+IF3GhBJOS/OknjuU/xcf81joO6Ty9P/ycfRsijKXIt0IZD8jvru9XhAuPp3ESnIcFifcL/of99ZpDevq2oPI39u+p8I9PL3eKHri+02/Lx5hB5f78i56yprxcycm1F8jjRPBBWYN6mYmXRPgRy20Sjhdd5o2h+JHNfTeLd1euAcgIEj4nGeEd1F7IFnjmxMAxKswphfOUNEDCM76f6I6et23RpRs2R3zvxGkRPWuQM6+u9O5cc2p7U5BWUp+wBBtawUHhwJ6hze5fbtjj9iRRek7/rkdi690d/OMZ4mGCXO7byVlFpYB1BI3XQilBDvWRFqK4sSQNWCiS0ppbD6bYnkab5pJMsD1bZwqirMTZZiUoRn1uvLkfNmxdRyj38XB/0lfpTXkdJh2T8yI876ppnAlcR5rIt4d/l3DxxEfaZs5AkOKI4R0ziRfzRrYMaW7q1fXQaPXL4m6KDdpEpoRu6ys3+VH0Azag0xWziU8EsCvBuUeNgrLjsQ+0DOnNoA5zCscKPA9RuY3sgYaJIt3tee2+pI3k29ZyXaVOsjHK9qc5mgWz0norARQi4NSBwQGBXeu/KdSN5ALSbG33Aw9msFexmuW53a/PbuQePPl5HUUNMdiFioqHcmYbigdil1273c0yuZ2O+xgJ3EAGrtTEBhqwW7ZvyrJhZdqRASG2m8xLjSNUi4Na4lOq+IevGSOD2vJ6nUlbOQsDkVBVRE1TZFzzrmjBHojOJXOzAg9GJWaW8FSYG47dgpZNJYSeEa0U+3mEej32p77uOkNXAznafVdp/Zct5a8PIx/nfWD1moRCdxIkGbgORNQ4xB3Ctbgthnri15b+DEZQ99653MZrUidldmAII7Or6EFZaBefU6dKeuiY26gb8VAtW/b7rrXDhFFqPZk7pO646CRLncp9xxRjSO9LXnXJPKzi2NYgvkP0dk+kPu9HIHp3h9RJBBgEBzYuSRLLNGytmrBqXqyMGEUiFxttgRWTywDSWJZ3xW1L++MtSWbnS1gxynJhciW5SxLViRFD63EYLaVVQpOIS+Qh75YVVNxFUrTaDlMhauUfHqv1lbwssoRJwFbd+PPZyjp7dVMTILy0RmXXWTWXl98kbBS+nBwe73Yrnv86fF6r1PkSvigPdKAfVLIZ/pAJJGQ3dB7Ll0j4q+0yLsvPtz4BFElFlaCPwryvjvJeKjNjhTTPCt5zmhx7DkUQPW4J+S5CvlV3a6reD4kjmbHL668rrfRG3oOKA9FVNjbsS/Fuya0rnBm5O0QLYSKLpcHKge96uDJ7fhffdrWo/EO+5q5m9NW7rscruX6+W/z6HrrXCqfCh4cwaojat6WmNoUdi4ZSip4sqqo6vbJLJgioC6X0cSEfJ62Eh89ZAyqGhszo37iINg8Q+v14Dj8Y9pRzeopJvxVcooKImAurmpYODOvZeH1sk1s1M757nV4HnOn5zq3MVk9RYUB+rWY+Ghjn9/QeIsguLle3h6FIfjjz55VxKBX/vb8APkyKSf1JKTSeX9lBrp7PqdFt589zhIHFANCY2gSMdn5eHtjyurx46xSV2WVPtGvLkz23TiYiNOLCR79L+HRGt3b+R1/jW0vX5W02wvsqtcT03rPAgKto5/v+6f2fT0Wn2yjnTxxP3EFeo46bcuDunEufSTraXlcSiqa726pfFft4gevSfPyQU+poP+z7uxCbrt4RYwXb6dJs85RXaVSwlKe0VyqkH9vm2pzlguchlysh0h3PTDSEaUmxEllrGNaiT/w+VLnN+k6p1VXvtQPvaBbj1NeL8sWjKQRIP2Xy6RCHqois9X4OIUTGQ8fc815yDwl/UBSiSYIRw6S3/8qC2jgXQdLii/8WGGrCZ913fvmzOondpad0fd83Le1xw32QIOdtNYStfGjuQJdr7a+XW8VxKZ4+1YxNcFMn8IXTLXI3KKUwb71b+Krkh8ih1XKVl97MRroogGWSw7+lJZMHjNHcQfv9bsuqzkuhFFZlrLjo3SdKEiZ9P5U3/Z7/D3u0PH7PhNf5Ny06J4fD2p9oHjIfIfoydUdkzrnZk/g6c0b9EBGofypJkHGBWqwYifNqzZV/Rc4q7N4YA81UAg+Qb72cN69z8jK2pJGQR7/uPMj1UWhB9ySiF76+g+2il4oX34/jD7Wvg5uI9OFrqR3EwOIvtH4YOJHiz8lxwNTfUqPV45khoBrvoO7moOaJgJzCJ6Px+LJuO7UaASSd76aN0RGy3QNSmhDTLso32DeIo9KClMBrxTkw/l6SzppJxwn9imKj+m7S5yQBm7dVpKoYY7qd8grqsDhhyD6XOsSvp+tPxG85W4tOWVtIgHQbcg7slws32yUZRQcr8vHMOrDxDhhXvdE0QNGRQNwGvEyXP9lfO9MiGoGKUO3BIVSvvgEox1yOpl/tAdeUVmwHJwXYd7pPpwO8DTWgkgHmf1etRnuZsqlpeluu3iY7dT1LHELHB3LnZN9RA98HrKy6SHuRE6mR+E8T68VkpE+vVBo8S9ffBId0UkU90tsrJFAWB3Q5E3Q+PfXHM0ZSm2auyG5opumiDLaSrMYs9SgOMQyZU0ISQPVQtQ5DvE6annAonSeLvKD0AzfFdfYRMo9xnyaQppb5Hga5mYfuByKePL5xPCdWde9TxJzPc9+DPg+VEOScuCj/hgFoCyCkUho32IVnK0QylnUDnD7Mm7bhZ5phtxV/AWgCQAciwkgiFCEGETgU1EYMtge04copxLiL3J2FEbRLj5exRYjRyPRwsT6sh7pNIfK2W314eRTk9x8+phpae4+Df26fq0WHZBQvUKtOnxFKfYmWmgExHKiSiyPTOgSutRiGl2QAh/z16nq29s5GIo0pi7xLqCJOBBwQ4z1GdX85bkcwUSxkUQUTtz9ZbR72m9rpm4eDiwD4oQP3noyBFEkX6EFX53Yf6JaGPp/D7zL+VsWaq30abSORhqV6cajaCF39qSSBz5sjoUX/Tc/i2C7+M5h/FFFHCCCehrwf6uQwyKPZrlqsyXlRpYKjuLf+6Sfvy7SrNOnLb/1DnZ7OIhTnMIN1UX+wdP7j6BfXSoT1SGvng+FJcsAfh7lFpplPC5YxgajDasiXEKR5qiQaq5iUZHY1nhhpxb6lLGBTBUNxFqFGpvvcLzRjkbZs1Dw4ElP9E36IAoSPM1jPjT3uZ+iUtD9UOcYkSBFj1Dr0hyhcQPdOGKSGJWQXGFQwnnI8BzRRnfL8nxD28BtOksgbknh+BjteMebgekVJNukJ1SeWBSLAOeZQBbIL69Z0ZE09WckPPD2Gc9YMMyihkYEAhMVSwSWQ13eWcLxN2g40Q/CHcvuHWDnBagBDfc9CWvygsYmtNDIhpqT8UhKPb8qv0wvHLJZY4gbAGUAYRCMBxAArzo7e1Mzx52VoVKQex5HRlFDBaATgwQ84Z2IURlECew+7YDpmblvvPMsN9N553sAo7Ag7lC4FQv//UwJFKvZ06gasTEOLKfBoEfjKe6shAmw+DGxvp5QrpxNn3e3CyVKi1BrsL+Er05J5QxA7hIB7YJIhBrp0rwTI4fR/hqH1zyfjQh0jIMiHJIVke4/iBcKT8RD7oaZZF0ZAkCKsNR1CSkYaOU1HDYlswQadnmkXaQjJCiAsLCRMlPtQ5ICMmooQLxZGoPnSvpYvo/oiSI08qhIaxzTMsJRJhaU6pXUsSrpdOsdOY2tVVqoJnjQUsir9hsSJDMw73LYo1jIqcEw3tnTozZEEm8qkbbVjRYlaawmRpQ8RwZvss6WczigcG+RYHAa2Cw6zGgbYv8bCoZ4rV3JzZBRDJYBwgGXrlH1sLxYeQWwMZvaLA4QrBYej2cYpDGLJbQgpVSdWTskCuIFSTSTEihUOcOZSaQgsUU0ysFA8jiWvidUTIhB65AcDEyRKDiSIlVEFYxLysxwpURBNKI2GAdw8EvGdZ4zu8ydHk3nbGc2vgt2bGREQKUKqmUKDBllkhQ0lXVlRMNUmSiWLFI+2YGI20tlQd2klZu5BsjTTaLaGzCgqm9ozBlQFJszTjAV2ZYCsdIjIBUYoO0Qykt73QXHat6qFYfhZKMSdkFRizbx4ERZMSLDDEopUqLjB6RhlrccMjS0ipC4MPJihSxpQG6QY0AO6FbceYbQDmbnHI0RAhckhtM6KtDTAHeDpAhHvA3F0RyH8lBml1DERuBCa2vlmUYjvuEVKjc0tpbii9re5Tn7ejDuMWUYKCUlUwUILSn4bPAiAsz7DZnVmK3qY8hNyExJc7M3MEAUVTBBg3s7AMFmgFg1BsQg/cK+TcCmR7gBSQY/YhqN+du1DoETb5VKEpGrBePE+4qH5s/uVOsZ8vH5dCpZgmksb04cgQDjPacDnp2PcMwcZh1haahTprLPm0zPiAVMUiJfcSYBeB+DZgIWWpNNRSmNXophpEyO3ZM3alitRNzKHz2eVUjvrwmoRvgc1sZbvh8PQlNbb2+yM5fpRhuccEMWZugOQCO1PuWbulEstePwtAuo9xxvB3Jl9NqLHrWgHIXiARbogqZdj3LkNkICywqzMOtMiKgsVIlD3YNQkG6zdOzS4SJIJIgyfRYTtTzu9u0uWJkFmPOJdlaXq0I2vXkRK6Id0lQNBRORD9GemNwrLe1jhYOu4r36fyQFBR6U5vuu+ofGwYMJNiMgeG4Dpbx5FdtUD3CJFJQzByCQS5DURbppJ33ueX6teVZovap3X5g+i3XdJwSdS8spzRkQYmy/qVm+nr9p3csDj6QiuO9EZQQ3vhmC6GjUunl00YpMFkOzD6dE1UmFBf6DLRDfRbTMGv5j0ztbanCwwFP1zxET6evY5vN5tRTAn3KMrn5N9mEGdU2TLLwghqOANnxKsQjTM+pAzTI8GYNVbrZAwhGt3Krr2K+RFq0oto7CJW+gzGB3ClXs0VwjNjNqilJhgonSArR4AOwbWQFyNf06qbCX6E9r35vth52t4NcjclB5jyHcqBKLghdL3GUQBakhmCIZrk9m6Hqaf13E9xTdtQU5kuB8dsRSKQ8Jw9weoDA6M+MPTtPMNjkeNNE9Rp9u+SdtD8yUNg90Sud5Z7+o7gayEHF3zRaNBGjpC6d6Ck6OJOEUTrc2IOMSwKAgLmx98ppDt+IEBMEEw1ia7lt70VlLNEqxVqG5lp6tw8tWuX6hDkOoctpzQF+aByQ2PPDo9/bk+evbGhcd9XXDCUsSseSmckOWwuJpwrSiHLoWWo3p207DIA/UcNmb7aboralNVS1uZNO01hix19AmJiHhJEeJdbd+bDeb1PzY7bAYymkmapmNaMPs5HKmymhGOttScsZrWsaXcFR1MlBoLR25M6Z1TDIpAvzpeX2O9742sEqdqXW8nLiyjCdGng58SWZAnQP6bMHB9kK6/ToBxrOaac8NgQuFJkjubULYg2CJ95KQPpEaRLQJEzfj7TNxcoPTw7nLF3xWVypnC02DvGSKOS+AoqBmGZ31Pvo5Yw35d9qLdMXjCEx8T6nvNhg4msDhyyl30YG4Av85DqX5Tu0Q3zVWBYue+k8OpGLNVi4qrwHAw6PoEEIMohFdDKvbZLWqgka8e+fLW8b08/qt6RHr2DtzDLdCF2QObz6SruANxYW9pTeaa+LFAQ7p7CK/XVUE9v2aL9In3QtBqKY4oDLx71ISaUJUZAh5ufQJ+ftRSSsiyURa/mQntqwnq02zCFSRSChBMpWSojCoFSqwiyEUJaisZKUf3Uuvs+JDyPyMPH3EoN6cRcQS1iB90SbHEWJD6O1ZF7iGYkhzJ1602DYpXEJFPatgW0KyERnqKaChgmIIHc3zb2obqwrJdwKQKgn7b7vCj52Lp8/FL0XvGQkTdQE8g6HKQoJKLDTVtUENaFHPpQxSJE2Jg0RkMKpuQuOhGYIIvaHFTnTIc4MyDCGf725fxkKNg5wTZ8YtYPrdm0r5+gtWlgxVIKsWRGD9fSmRWpUBRNWo1GwuUsGus38bQ2DRCxAwBcAPkyQWChIo0ThItgB81FQVQUIqyAsgQUUWQBQkipISKMgyIsIjhityfe1QIxMVdiEIBZIvRKRNLEgZxhELkYLBEgsJEYMYpC5iSt9zZJgMhdgDhgaThNJqFsLKoIlk6J1IB5sgf9hhy33kz0J+N+mdvaW2DRoKVbrALWrg+aR4l8aMMKNqEJl4trCEEtneih4S/m6Kt1X5jaiKG2N0Ptqlw228jKoRiIiDIoIsYwSKopFAWAMESCkxch6QhpiWnGu6TAHL7jQ8qnSdzxfPzsJboyHLv8GInc52CyOd3YJg98zWQ1Au01qFy6totmvHI6H2+zSskvUnPyJ2yKQrBZEcZUDnllKh0h5oR+2InRDJ4x6qZnQOpIG/gkA7rVsBvyjtvhELr86FzmYK5nhB9zswMBo0d0wJFWYrItYVH2wwMSStZpAOux3/DIeyGSbIL5BD56lAdrK6betemuDiZemshyeQj6j1UMgQMvZd3R45q2pQy6wFO+0TcqzWzejb+nGbjeRbn9KgdhZW+qHUK6g0QjRsnza6iP4PBKL1a9RW1GhnDWwzDU63nJSHR7gBxgSp1ljfnMmoGIyekQqfRAPl+1QqLzmeZKTukQSRQFirBYCMVQUjEiokRF7JRYMiiMUWCIo+TVUVSRERkWCiKCgqoKCqsRRWFmjXmE66SdcP5mbAcH7YL6gwqr8OxzhhqSLEiqdKEKhCVEqLBkDQqowRFgyKraa/nRTucAnSqOpWr4MiPK94GaeSjc7lgDkrlBk5yoM9Sjjyp3opTriiMvyUTyQiHpzOYSZm5MjkAyPQsbASXhTsHXR151pHImo5OMuDr6+UvCph4u7wWOmDAGKHE0wU7Q4u3Ie5t1BUOpIbwqSQUtgSbFh96AoWY7n2/C+PCU5xz6a2NcNsKXjcO7CEkFIwYo+lovugsKM6NYxRy0GIskVSZTLrRoZpy3EbfMTbR9ueuoGQ6BHc1ciJWd6eNsgxRIw2uJolaDeJIEQ5evHaiBhkXdWFsm0505tb0K3ODlTJ5PdkNtHCaOrvyhaHY9iQ4DGPz7rrHUBoCkO0WRAtR+drQyC5Z0SnuQvbIdMJtA6B7VydIJ0BQNlgqxVjzon4Its5DUPgiwzEzEYy0kNzI/RyGodOv2sxHpfQlpqG1DuQgR1BMZ0lExbPznrsZXq1Fu5rmqnMzN9GUKksCZeiq3dzHfLk1eEmEiLBFzEmqehRkdHnXFkNDwQILgoKXlxXVqF2uazE0mImC5cwrErJpkS2YGxl0rM1akrNKh6fCbhsWYyCIFx2QgYaWYkSKpnRBlETeIMAUBhQYgBfUMBrYqmNqKkdKI3UMQmNLaQfyjvabshmSK2Qiw1sO3Cum3FkoG7oP0BRllBrZbr0oBSBYpMFBxpNUWG+xz4KLDxGs90KkRCp05WG6TiciGodZUyksl7zJrsbMqbMBYXNYZq6ca1Bc3sayHCYhtkdURLo+N4G+9Ehb20svklgm9C0pTSUwNYVmFZF++mA41lp2SjgMWbXloupp4tGMEZoRmhoBu1JNaWmIIKyxLJlosEEE4pjpurvlMzRkzVoFYNojJYOMJcQwUULADC3ViSKI8fMTvpk5JOEzxxNBVdx5aEDOKnLIElMgq6IoGmBu7MUMpNGy0hUiISUySGhhKhQjVN0UKRQfbZDjjCbac8wyagZcYyCBq1KmjgBy55i2C3EZIQUc2ILCQEWMIaogMUVgwRrkXMjx0230vpkWGwYp0S4ECBk0x2B+TtScQfRhWToMttRZAWHvaKSfWf1p07dl7Wy20iCilRGBUktqKgouJco5wSy8KI0xSmgyhZIWKCrD1CNQfMYahskWQWDEkVQirARIoBqYoWGCkzFSHGqG6LBdem+0jMXu2FygWSwuUWNhciSJFJ2btuArCqWHOABiJIB7OsjHzj8SL+gIHSfSoTOlQ0Zb5ZhUpLaSZQ1QMJBYaZCsETeDWGIa3sKkzVJNoO3nYYZCYqgcUCJlv0yWWW9AhxEn2/YV5TF89At8RD1gP2QqT6yA/hFHngRyzR2VHeKsgMgpIIyKgfz8RICcnfRReZ86TrPQc+SkhHPL8o+G2euDCnMgBA0ooPC5hc5QKtDXAUqeAjnx0gMisGAoCwVZFFCEVPgkvNkqelKREFiwD26AUJsRIKCnIz630kgklPz0SmYunLyd4lZXPyxNQsKsZm0gvSMCKRiyB1O8jrqLlb7dW7e6mZLWB739E2kk3iEFhSezP40qH3tVQYZGwWOUsYqMX8dPlgUe+2HNhpCp3ykRFHltKuEU8vXjJR0MB03j8lXHhKZQfFnDJgYsEQYhvRpdEWdpRQ7glMISgkwTwZL0+EcEt7Fj8P0hwYTZNFRcA92KctjyVO5myEjyAxzKsSE+EoJAqFSHpG3oUnZ2hjhPfBUwvxOqL2jOe+8BSKib0+4IfgIoBFZFVIiSCQivvydpOCeTCElVXbyHJM3SIvKfLukZBGIRYZtPqOPv+4rsh04DuYHbRkE+1wieZoTvKPKH7IlWT2WykbOQcef3ac9hz9vSe2+/GST1DGmaKDvRaAKsRgsgsiMX7UKVmart3NjWAfoPoaTj8NAsD58UKqExUIBkxnXDZdtq6A4F5Jl533jyyS6Y/MYgaLVHLCV4zaSGoM6l2jouYKozA79b4O4T70JQaDDIHwVO05Fh2gM52WV2ZVEi92SpA/KnqZQBPjSeICTEWEUjacfUO1Pj50DtKtbc3nIYpPkNTlOJwEkziB9EUgYQ9GrEtoJ0tMsKqIoMGINrZKEUC0aFYqwQVBa1BlapFjaTC0MGXLjMaICINKSoKYyoiIopbhjSoKE6WxXEKIrRLLSY4KpWZHV1MFKV1cjkMpMFQxqKmJVRRjFYkVYRGKMVJlmOGowoiCKiIlaiqggMSQIUZEN3JdRvRk/KhT2Cj3TANBM3UZBnqTGMxjqJkZRuREIDiwoSdCVyWyWkQNJMFSYwcpWatrGZdJNCSpchodUutJU0JiKsO3hPqddz8bJ3v7PSsB2ZFWKsFnd9x6BxI+1dLNWgoVdu938gziAcVSFpZvcMwh/JzovE5iWhwkSFlcl1h739aQyga9zZDlDJ1VI18JJsWDSSDYkahV8kdgOqFL6IG8CyEQZPbVTJ90gckEZHmqoOjcL+hrtxytC0ncC2HGeK+YZGpiChiCgIgLBWWxSLFiDA3slGSEqSndkMyHwFUYosiioqCAiqMEYIsUBTpJx4ZCWHpiiGUA9BlQ9g86BPE6djsSnlAEpkkPLMTQzRcwXAZBFVjSkIaLhjog43AwCyS4FJjWTGddz4JDUDdhvvXuPGrQoHHhVAxYon9vTudYqDKkfU0j3PYPhaNeJs3cWMVHAqIiDWsoJGU2hO6ps1k2k244viN6ziIihQRFvMltCerEMXrTirFm9NylDUelbovLkMTUwysXSpu/QrExwxSja6odDdoymKabuWiyxiUNveZdNVrZpV3CQkkoSB5WnGpMKpkTljV1uTdWVLoUJ02rq4KKQiBThOKkUbHFWPbcqq6duiB+jtAmsQRDOnHfV1EFq0U5gjLyYDgdnZmbR83kSmXZ5amMvaMTCV5BjEs293btmXWAt1RU9kaMk5xB8cuLmg77l4hI0QYh0aYEgv5M/adQrlAlvPJLwqQjVoUIinnnk3V3EXDgoGTXnPBLeMyzFSTcvIw4VfXAqywOqOtAtocHeCjo8/lLDlbaemGmYJul2Ghlos0oBKBu6aUKnDqSU3RViu2KRFhRLu4Ybsqkwh+ThwmWQqMFDowDYnCfgFgNxdniZ9SxLkgOkxoOzt73DGsfXTbY2TV1y4WhJEq9wLppJffGRWWRZyT207LmDdDDSpI8ghDKWS+kRyqM7RCNVxoEa7M0dPAKLHLU2MswmWFjFOuZgjJwlCxVoQzMlVLNOyqoqKGHdUGIHXeh0XUw6B8rukT5QWiJoXrhLCMQObFndgoFaFtyqIEcYwe9tDCLSYsaCtDPK9LbxIeNzf4HSZsw0xGM7DwWluG1FWV2W3G+HSC/KqQh7s0zDs3EMRylQxqPAcKfHBJKpCrlVXsnu9dKcpIp4d7Y2ZMyiYeIclt/nUtqhsPAGjUTI2aKOygVAFxsBhMzLsDD6Ku6q3WWWclxGjo6NXdvOgAjoKhcwwgQk1QYLg/yw9RwgYTY9GmMXYzgoiVmeFBx14XmbHlgzUQw2CWoQnldETH4mgXJaQae9jEFYOogOTuDTyWwVqA8SiZDk0naA72ghUdTQmTJDbEzIzLEBxtE3+qam6gaZF9cmSRIayzDhCGEwEZBRwu6EkOcMvouHNci4T4pIYnWXaxqUuPYYDILYED57RBOAZ7Ig5dTIzCQ0hud9NzvDsqMZEVARgXocvEmuzhwgejp0vXkCLBpwECTpAcA0QhTD21PUWQFGaMMiy+ZepdeWgoESTl08oF4u/zpQ47am+xIlee4CdpIabQFJBdoSqwJFgVkKMkFIopAUgLJIiEikBSAKAsIsAESRZF67HxHeZUcVDErUCxmYVXUp+hJZuhUmj7MGYENJIsIpFITfsAWOsTlNEiwhwtcnPpQQ3UOQmMBUgQThKWNgbqZsnUwxhhLzIj4xoclfWQzCAIcZiK8WqIsyNNWG3JswTGTSRxkq6d3FRUYWSUGpjW76LhU0S5cVa3YGHFNsSF0IUSny6SExUh5IIgLAh9GBiRQxIClYFYRgtjlqbpMmtYhbY8BZ1OuZUDaLWZREN2RwhZEDlbOx2oVQ8tvG0M2K/DKmVFS5pk9vE17VEgSU1lEEoinjvwJiQC4JgNs2N3ee8hL9TpQGM78Xzsu2qVEoVWMu27uaHXYhJLRn7R6nyX/6qPfCfcQPA160BQGuCkcolIPMErY5Tdlsxsg7W3s9nuBhXSxj4wOw7BvoGSwcwO2mshLA9kJPRWf/diwOJp3xDleZMnugB5iQh6mFDRoTCXfYnbGJoYegDjTr9Rg8+k+tEqEhtHpBkW8RqJeBmmT1Fw87YOVVX8LjMVMc2lkXhMnbqAcb7Sfl0FIaDwZAvtO4e3uZ6u4ozdmsMysFZWhbZLQTlEpIsyxT1SZkl5Qy7oQFOtKeyEFmT8tZq7kkKMbQDENLrki2bMwDsGg31vsNNllLUakKMwyoP1mTh81GIF4JdtRvaoMBvH5wKiL+q9Ia4TaoFlcRzi+6AOpmM9LIYgMitoN0rjYhRrJUgVAWSUZDB6ztO05bqnIiVFCF+/jr4cSrl51yDK+LXJVnECgUX8+Kt4b8UmsOoL5Q1FgjITW4ZWl+pCT+gsFokjKjHeQZLwybZEUoLOUXMxS1BDwROVijNjUhVWlSAq7LhWQKmVwgqxWkySuQEHF0YOBMCyKJoEnCBmHFxIUkASQQ1G0iUXL2jdIJ6jXMGTTXtEmzUl93FGBP5rHZDGKHbV/APm3aCB2cLbdMJ5F3ImXFr7kdRB8oh5QWoI/bFKgskgHN6biu6bEsvs97DcPqU//F3JFOFCQhJGJ7w='
    return bz2.decompress(base64.decodebytes(licenseText)).decode('utf-8')


def outputLicense():
    """

    """
    print(returnLicense())


if __name__ == "__main__":
    outputLicense()