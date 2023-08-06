# from scaffold.command.edk import Edk
from eclinical.scaffold.inputs.component.radio import Radio


class EclinicalUri:

    @classmethod
    def input(cls, edk, msg: str = "请输入访问的eclinical地址", select=("113", "97", "115", "38", "us_dev", "us_prod", "us_demo4", "shenkang_prod")):
        radio = Radio(msg, select)
        try:
            key = radio.get(int(input(f"{radio}\n")))
            return edk.eclinical_serve.get(key)
        except Exception as e:
            return cls.input(edk, "输入非法，请输入访问的eclinical地址")