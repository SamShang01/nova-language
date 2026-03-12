"""
Nova包管理器 - 包发布和安装
"""

import os
import json
import shutil
import hashlib
from typing import Dict, List, Optional
from pathlib import Path


class Package:
    """
    包信息类
    """
    
    def __init__(self, name: str, version: str, description: str = ""):
        """
        初始化包
        
        Args:
            name: 包名
            version: 版本号
            description: 描述
        """
        self.name = name
        self.version = version
        self.description = description
        self.dependencies: Dict[str, str] = {}
        self.files: List[str] = []
        self.checksum: str = ""
    
    def to_dict(self) -> Dict:
        """
        转换为字典
        
        Returns:
            Dict: 包信息字典
        """
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'dependencies': self.dependencies,
            'files': self.files,
            'checksum': self.checksum
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Package':
        """
        从字典创建包
        
        Args:
            data: 包信息字典
        
        Returns:
            Package: 包对象
        """
        pkg = cls(data['name'], data['version'], data.get('description', ''))
        pkg.dependencies = data.get('dependencies', {})
        pkg.files = data.get('files', [])
        pkg.checksum = data.get('checksum', '')
        return pkg


class PackageManager:
    """
    包管理器
    
    负责包的发布、安装、卸载和管理
    """
    
    def __init__(self, registry_path: str = None, install_path: str = None):
        """
        初始化包管理器
        
        Args:
            registry_path: 注册表路径
            install_path: 安装路径
        """
        if registry_path is None:
            registry_path = os.path.expanduser('~/.nova/registry')
        if install_path is None:
            install_path = os.path.expanduser('~/.nova/packages')
        
        self.registry_path = registry_path
        self.install_path = install_path
        
        self._ensure_directories()
        self._load_registry()
    
    def _ensure_directories(self):
        """
        确保必要的目录存在
        """
        os.makedirs(self.registry_path, exist_ok=True)
        os.makedirs(self.install_path, exist_ok=True)
    
    def _load_registry(self):
        """
        加载包注册表
        """
        self.registry_file = os.path.join(self.registry_path, 'registry.json')
        self.registry: Dict[str, Dict[str, Package]] = {}
        
        if os.path.exists(self.registry_file):
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for name, versions in data.items():
                    self.registry[name] = {}
                    for version, pkg_data in versions.items():
                        self.registry[name][version] = Package.from_dict(pkg_data)
    
    def _save_registry(self):
        """
        保存包注册表
        """
        data = {}
        for name, versions in self.registry.items():
            data[name] = {}
            for version, pkg in versions.items():
                data[name][version] = pkg.to_dict()
        
        with open(self.registry_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _calculate_checksum(self, file_path: str) -> str:
        """
        计算文件的校验和
        
        Args:
            file_path: 文件路径
        
        Returns:
            str: 校验和
        """
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def publish(self, package_path: str, package_file: str = None):
        """
        发布包
        
        Args:
            package_path: 包路径
            package_file: 包文件（可选）
        """
        package_path = os.path.abspath(package_path)
        
        if not os.path.exists(package_path):
            raise ValueError(f"包路径不存在: {package_path}")
        
        package_json = os.path.join(package_path, 'package.json')
        if not os.path.exists(package_json):
            raise ValueError(f"package.json 不存在: {package_json}")
        
        with open(package_json, 'r', encoding='utf-8') as f:
            pkg_data = json.load(f)
        
        pkg = Package(
            pkg_data['name'],
            pkg_data['version'],
            pkg_data.get('description', '')
        )
        pkg.dependencies = pkg_data.get('dependencies', {})
        
        if package_file is None:
            package_file = f"{pkg.name}-{pkg.version}.nova"
        
        package_file_path = os.path.join(self.registry_path, package_file)
        
        if os.path.exists(package_file_path):
            raise ValueError(f"包文件已存在: {package_file}")
        
        shutil.make_archive(
            package_file_path[:-5],
            'zip',
            package_path
        )
        
        pkg.checksum = self._calculate_checksum(package_file_path + '.zip')
        shutil.move(package_file_path + '.zip', package_file_path)
        
        pkg.files = self._get_package_files(package_path)
        
        if pkg.name not in self.registry:
            self.registry[pkg.name] = {}
        
        self.registry[pkg.name][pkg.version] = pkg
        self._save_registry()
        
        print(f"成功发布包: {pkg.name} v{pkg.version}")
        print(f"包文件: {package_file_path}")
        print(f"校验和: {pkg.checksum}")
    
    def _get_package_files(self, package_path: str) -> List[str]:
        """
        获取包文件列表
        
        Args:
            package_path: 包路径
        
        Returns:
            List[str]: 文件列表
        """
        files = []
        for root, dirs, filenames in os.walk(package_path):
            for filename in filenames:
                if filename == 'package.json':
                    continue
                rel_path = os.path.relpath(os.path.join(root, filename), package_path)
                files.append(rel_path)
        return files
    
    def install(self, package_name: str, version: str = None):
        """
        安装包
        
        Args:
            package_name: 包名
            version: 版本号（可选）
        """
        if package_name not in self.registry:
            raise ValueError(f"包不存在: {package_name}")
        
        versions = self.registry[package_name]
        
        if version is None:
            version = max(versions.keys())
            print(f"未指定版本，安装最新版本: {version}")
        elif version not in versions:
            raise ValueError(f"版本不存在: {version}")
        
        pkg = versions[version]
        package_file = os.path.join(self.registry_path, f"{package_name}-{version}.nova")
        
        if not os.path.exists(package_file):
            raise ValueError(f"包文件不存在: {package_file}")
        
        install_dir = os.path.join(self.install_path, f"{package_name}-{version}")
        
        if os.path.exists(install_dir):
            print(f"包已安装: {install_dir}")
            return
        
        os.makedirs(install_dir, exist_ok=True)
        shutil.unpack_archive(package_file, install_dir, 'zip')
        
        print(f"成功安装包: {package_name} v{version}")
        print(f"安装路径: {install_dir}")
    
    def uninstall(self, package_name: str, version: str = None):
        """
        卸载包
        
        Args:
            package_name: 包名
            version: 版本号（可选）
        """
        if version is None:
            versions = os.listdir(self.install_path)
            versions = [v for v in versions if v.startswith(package_name + '-')]
            
            if not versions:
                raise ValueError(f"未找到已安装的包: {package_name}")
            
            for v in versions:
                install_dir = os.path.join(self.install_path, v)
                shutil.rmtree(install_dir)
                print(f"已卸载: {v}")
        else:
            install_dir = os.path.join(self.install_path, f"{package_name}-{version}")
            
            if not os.path.exists(install_dir):
                raise ValueError(f"包未安装: {package_name} v{version}")
            
            shutil.rmtree(install_dir)
            print(f"已卸载: {package_name} v{version}")
    
    def list_packages(self, package_name: str = None):
        """
        列出包
        
        Args:
            package_name: 包名（可选）
        """
        if package_name is None:
            print("注册表中的包:")
            for name, versions in sorted(self.registry.items()):
                latest_version = max(versions.keys())
                print(f"  {name} (最新: {latest_version})")
                for version in sorted(versions.keys()):
                    print(f"    - {version}")
        else:
            if package_name not in self.registry:
                print(f"包不存在: {package_name}")
                return
            
            versions = self.registry[package_name]
            print(f"包: {package_name}")
            for version, pkg in sorted(versions.items()):
                print(f"  版本: {version}")
                print(f"    描述: {pkg.description}")
                print(f"    依赖: {pkg.dependencies}")
                print(f"    文件数: {len(pkg.files)}")
    
    def search(self, query: str):
        """
        搜索包
        
        Args:
            query: 搜索查询
        """
        query = query.lower()
        results = []
        
        for name, versions in self.registry.items():
            if query in name.lower():
                latest_version = max(versions.keys())
                pkg = versions[latest_version]
                results.append((name, latest_version, pkg.description))
        
        if not results:
            print(f"未找到匹配的包: {query}")
            return
        
        print(f"搜索结果 ({len(results)}):")
        for name, version, description in results:
            print(f"  {name} v{version}")
            print(f"    {description}")
    
    def info(self, package_name: str, version: str = None):
        """
        显示包信息
        
        Args:
            package_name: 包名
            version: 版本号（可选）
        """
        if package_name not in self.registry:
            raise ValueError(f"包不存在: {package_name}")
        
        versions = self.registry[package_name]
        
        if version is None:
            version = max(versions.keys())
        elif version not in versions:
            raise ValueError(f"版本不存在: {version}")
        
        pkg = versions[version]
        
        print(f"包: {pkg.name}")
        print(f"版本: {pkg.version}")
        print(f"描述: {pkg.description}")
        print(f"依赖: {pkg.dependencies}")
        print(f"文件数: {len(pkg.files)}")
        print(f"校验和: {pkg.checksum}")
        
        if pkg.files:
            print(f"\n文件列表:")
            for file in pkg.files:
                print(f"  {file}")


def main():
    """
    主函数
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Nova包管理器')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    publish_parser = subparsers.add_parser('publish', help='发布包')
    publish_parser.add_argument('path', help='包路径')
    publish_parser.add_argument('--file', help='包文件名')
    
    install_parser = subparsers.add_parser('install', help='安装包')
    install_parser.add_argument('name', help='包名')
    install_parser.add_argument('--version', help='版本号')
    
    uninstall_parser = subparsers.add_parser('uninstall', help='卸载包')
    uninstall_parser.add_argument('name', help='包名')
    uninstall_parser.add_argument('--version', help='版本号')
    
    list_parser = subparsers.add_parser('list', help='列出包')
    list_parser.add_argument('name', nargs='?', help='包名')
    
    search_parser = subparsers.add_parser('search', help='搜索包')
    search_parser.add_argument('query', help='搜索查询')
    
    info_parser = subparsers.add_parser('info', help='显示包信息')
    info_parser.add_argument('name', help='包名')
    info_parser.add_argument('--version', help='版本号')
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    pm = PackageManager()
    
    if args.command == 'publish':
        pm.publish(args.path, args.file)
    elif args.command == 'install':
        pm.install(args.name, args.version)
    elif args.command == 'uninstall':
        pm.uninstall(args.name, args.version)
    elif args.command == 'list':
        pm.list_packages(args.name)
    elif args.command == 'search':
        pm.search(args.query)
    elif args.command == 'info':
        pm.info(args.name, args.version)


if __name__ == '__main__':
    main()
