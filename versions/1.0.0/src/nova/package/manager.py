"""
Nova语言包管理系统

负责包的安装、卸载、更新和管理
"""

import os
import sys
import json
import shutil
import tempfile
import urllib.request
import zipfile
import hashlib
from typing import Dict, List, Optional, Tuple


class PackageManager:
    """
    Nova语言包管理器
    """
    
    def __init__(self, package_dir: str = None):
        """
        初始化包管理器
        
        Args:
            package_dir: 包存储目录，默认使用 ~/.nova/packages
        """
        if package_dir is None:
            self.package_dir = os.path.join(os.path.expanduser("~"), ".nova", "packages")
        else:
            self.package_dir = package_dir
        
        # 确保包目录存在
        os.makedirs(self.package_dir, exist_ok=True)
        
        # 包索引文件
        self.package_index = os.path.join(self.package_dir, "package_index.json")
        
        # 初始化包索引
        self._initialize_index()
    
    def _initialize_index(self):
        """
        初始化包索引
        """
        if not os.path.exists(self.package_index):
            with open(self.package_index, 'w', encoding='utf-8') as f:
                json.dump({"packages": {}}, f, indent=2)
    
    def _load_index(self) -> Dict:
        """
        加载包索引
        
        Returns:
            Dict: 包索引数据
        """
        with open(self.package_index, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_index(self, index: Dict):
        """
        保存包索引
        
        Args:
            index: 包索引数据
        """
        with open(self.package_index, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
    
    def install(self, package_name: str, version: str = "latest") -> bool:
        """
        安装包
        
        Args:
            package_name: 包名
            version: 版本号，默认为latest
        
        Returns:
            bool: 安装是否成功
        """
        try:
            # 检查包是否已安装
            if self.is_installed(package_name):
                print(f"包 {package_name} 已经安装")
                return True
            
            # 下载包
            package_url = self._get_package_url(package_name, version)
            if not package_url:
                print(f"无法找到包 {package_name} 的版本 {version}")
                return False
            
            # 下载并安装
            print(f"正在下载包 {package_name}...")
            package_path = self._download_package(package_url)
            
            print(f"正在安装包 {package_name}...")
            install_path = self._install_package(package_path, package_name)
            
            # 更新包索引
            index = self._load_index()
            index["packages"][package_name] = {
                "version": version,
                "path": install_path,
                "installed_at": self._get_timestamp()
            }
            self._save_index(index)
            
            print(f"包 {package_name} 安装成功")
            return True
        except Exception as e:
            print(f"安装包 {package_name} 失败: {e}")
            return False
    
    def uninstall(self, package_name: str) -> bool:
        """
        卸载包
        
        Args:
            package_name: 包名
        
        Returns:
            bool: 卸载是否成功
        """
        try:
            # 检查包是否已安装
            if not self.is_installed(package_name):
                print(f"包 {package_name} 未安装")
                return False
            
            # 获取包路径
            index = self._load_index()
            package_info = index["packages"][package_name]
            package_path = package_info["path"]
            
            # 删除包
            print(f"正在卸载包 {package_name}...")
            if os.path.exists(package_path):
                shutil.rmtree(package_path)
            
            # 更新包索引
            del index["packages"][package_name]
            self._save_index(index)
            
            print(f"包 {package_name} 卸载成功")
            return True
        except Exception as e:
            print(f"卸载包 {package_name} 失败: {e}")
            return False
    
    def update(self, package_name: str) -> bool:
        """
        更新包
        
        Args:
            package_name: 包名
        
        Returns:
            bool: 更新是否成功
        """
        try:
            # 检查包是否已安装
            if not self.is_installed(package_name):
                print(f"包 {package_name} 未安装")
                return False
            
            # 卸载旧版本
            self.uninstall(package_name)
            
            # 安装最新版本
            return self.install(package_name, "latest")
        except Exception as e:
            print(f"更新包 {package_name} 失败: {e}")
            return False
    
    def list_packages(self) -> List[Dict[str, str]]:
        """
        列出已安装的包
        
        Returns:
            List[Dict[str, str]]: 已安装包的列表
        """
        index = self._load_index()
        packages = []
        for name, info in index["packages"].items():
            packages.append({
                "name": name,
                "version": info["version"],
                "installed_at": info["installed_at"]
            })
        return packages
    
    def is_installed(self, package_name: str) -> bool:
        """
        检查包是否已安装
        
        Args:
            package_name: 包名
        
        Returns:
            bool: 是否已安装
        """
        index = self._load_index()
        return package_name in index["packages"]
    
    def get_package_info(self, package_name: str) -> Optional[Dict]:
        """
        获取包信息
        
        Args:
            package_name: 包名
        
        Returns:
            Optional[Dict]: 包信息，如果未安装则返回None
        """
        index = self._load_index()
        return index["packages"].get(package_name)
    
    def _get_package_url(self, package_name: str, version: str) -> Optional[str]:
        """
        获取包的下载URL
        
        Args:
            package_name: 包名
            version: 版本号
        
        Returns:
            Optional[str]: 包的下载URL
        """
        # 这里应该从包仓库获取URL
        # 暂时返回模拟URL
        return f"https://nova-packages.org/packages/{package_name}/{version}.zip"
    
    def _download_package(self, url: str) -> str:
        """
        下载包
        
        Args:
            url: 包的下载URL
        
        Returns:
            str: 下载的包文件路径
        """
        # 创建临时文件
        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        # 下载文件
        try:
            urllib.request.urlretrieve(url, tmp_path)
            return tmp_path
        except Exception as e:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise e
    
    def _install_package(self, package_path: str, package_name: str) -> str:
        """
        安装包
        
        Args:
            package_path: 包文件路径
            package_name: 包名
        
        Returns:
            str: 安装路径
        """
        # 创建包安装目录
        install_path = os.path.join(self.package_dir, package_name)
        os.makedirs(install_path, exist_ok=True)
        
        # 解压包
        with zipfile.ZipFile(package_path, 'r') as zip_ref:
            zip_ref.extractall(install_path)
        
        # 清理临时文件
        os.unlink(package_path)
        
        return install_path
    
    def _get_timestamp(self) -> str:
        """
        获取当前时间戳
        
        Returns:
            str: 时间戳
        """
        import datetime
        return datetime.datetime.now().isoformat()


class PackageCLI:
    """
    包管理命令行接口
    """
    
    def __init__(self):
        self.package_manager = PackageManager()
    
    def run(self, args: List[str]):
        """
        运行命令
        
        Args:
            args: 命令行参数
        """
        if len(args) < 1:
            self._show_help()
            return
        
        command = args[0]
        
        if command == "install":
            if len(args) < 2:
                print("请指定要安装的包名")
                return
            package_name = args[1]
            version = args[2] if len(args) > 2 else "latest"
            self.package_manager.install(package_name, version)
        
        elif command == "uninstall":
            if len(args) < 2:
                print("请指定要卸载的包名")
                return
            package_name = args[1]
            self.package_manager.uninstall(package_name)
        
        elif command == "update":
            if len(args) < 2:
                print("请指定要更新的包名")
                return
            package_name = args[1]
            self.package_manager.update(package_name)
        
        elif command == "list":
            packages = self.package_manager.list_packages()
            if not packages:
                print("没有安装任何包")
            else:
                print("已安装的包:")
                for package in packages:
                    print(f"- {package['name']} (版本: {package['version']}, 安装时间: {package['installed_at']})")
        
        elif command == "info":
            if len(args) < 2:
                print("请指定要查看的包名")
                return
            package_name = args[1]
            info = self.package_manager.get_package_info(package_name)
            if info:
                print(f"包 {package_name} 的信息:")
                print(f"  版本: {info['version']}")
                print(f"  路径: {info['path']}")
                print(f"  安装时间: {info['installed_at']}")
            else:
                print(f"包 {package_name} 未安装")
        
        else:
            self._show_help()
    
    def _show_help(self):
        """
        显示帮助信息
        """
        print("Nova包管理命令:")
        print("  install <包名> [版本] - 安装包")
        print("  uninstall <包名> - 卸载包")
        print("  update <包名> - 更新包")
        print("  list - 列出已安装的包")
        print("  info <包名> - 查看包信息")


def main():
    """
    主函数
    """
    cli = PackageCLI()
    cli.run(sys.argv[1:])


if __name__ == "__main__":
    main()