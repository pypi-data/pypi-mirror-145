from distutils.core import setup

setup(
    name='oh_my_tools_package',  # 模块对外的名字
    version='0.0.3beta56',  # 版本号
    description='工具包',  # 描述
    author='jeffery',  # 作者
    url='https://github.com/jeffery0628/tools_package',  # 网站
    author_email='jeffery.lee.0628@gmail.com',
    include_package_data=True,
    package_dir={"my_tools_package": "my_tools_package"},
    package_data={"my_tools_package": ["configs/*.yaml", "configs/bert_configs/*.json", "configs/bert_configs/*.txt"]},
    packages=["my_tools_package", 'my_tools_package.nlp', "my_tools_package.algorithm",
              'my_tools_package.utils', 'my_tools_package.utils.file', 'my_tools_package.utils.torch',

              "my_tools_package.tmd", "my_tools_package.tmd.base", "my_tools_package.tmd.layers",
              "my_tools_package.tmd.loss", "my_tools_package.tmd.metric", "my_tools_package.tmd.model",
              "my_tools_package.tmd.trainer"

              ],  # 要发布的模块,指定到具体文件夹即可
    python_requires=">=3.5, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3*, !=3.4*",  # Python版本依赖
    install_requires=["jieba", 'torch', 'transformers', "mmh3", "pypinyin", "argparse", "regex", "numpy", "pytorch-crf",
                      "seqeval","pandas"
        , "cos-python-sdk-v5", "Levenshtein"],  # 第三方库依赖

)

# python setup.py sdist upload
