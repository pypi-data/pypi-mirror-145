import setuptools

# 第三方依赖
requires = [
    "turtle == 0.0.2",
    "pygame == 2.1.2"
]

# 自动读取readme
with open(r'README.md', "r") as f:
    readme = f.read()

setuptools.setup(
    name="py_games",  # 包名称
    version="0.0.1",  # 包版本
    description="Some games on python",  # 包详细描述
    long_description=readme,   # 长描述，通常是readme，打包到PiPy需要
    author="ZMF",  # 作者名称
    author_email="zzmf20110806@163.com",  # 作者邮箱
    # url="github.com/CDT-1",   # 项目官网
    include_package_data=True,  # 是否需要导入静态数据文件
    python_requires=">=3.0, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3*",  # Python版本依赖
    install_requires=requires,  # 第三方库依赖
    zip_safe=False,  # 此项需要，否则卸载时报windows error
    classifiers=[    # 程序的所属分类列表
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)