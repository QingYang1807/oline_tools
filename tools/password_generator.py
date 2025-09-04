#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
随机密码生成器
支持自定义长度、字符类型、复杂度评估等功能
"""

import random
import string
import argparse
import sys
from typing import Dict, List, Tuple
import re


class PasswordGenerator:
    """密码生成器类"""
    
    def __init__(self):
        # 字符集定义
        self.uppercase = string.ascii_uppercase
        self.lowercase = string.ascii_lowercase
        self.numbers = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # 易混淆字符
        self.similar_chars = "0O1Il"
        self.ambiguous_chars = "{}[]()/\\|"
        
        # 密码历史
        self.password_history = []
    
    def generate_password(self, length: int, options: Dict) -> str:
        """
        生成指定长度的随机密码
        
        Args:
            length: 密码长度
            options: 生成选项
            
        Returns:
            生成的密码字符串
        """
        charset = ""
        password = ""
        
        # 构建字符集
        if options.get('use_uppercase', True):
            charset += self.uppercase
        if options.get('use_lowercase', True):
            charset += self.lowercase
        if options.get('use_numbers', True):
            charset += self.numbers
        if options.get('use_symbols', True):
            charset += self.symbols
        if options.get('custom_chars'):
            charset += options['custom_chars']
        
        # 验证字符集
        if not charset:
            raise ValueError("请至少选择一种字符类型！")
        
        # 排除相似字符
        if options.get('exclude_similar', False):
            charset = ''.join(char for char in charset if char not in self.similar_chars)
        
        # 排除易混淆字符
        if options.get('exclude_ambiguous', False):
            charset = ''.join(char for char in charset if char not in self.ambiguous_chars)
        
        # 确保至少包含每种选中的字符类型
        if options.get('use_uppercase', True):
            password += random.choice(self.uppercase)
        if options.get('use_lowercase', True):
            password += random.choice(self.lowercase)
        if options.get('use_numbers', True):
            password += random.choice(self.numbers)
        if options.get('use_symbols', True):
            password += random.choice(self.symbols)
        
        # 填充剩余长度
        remaining_length = length - len(password)
        for _ in range(remaining_length):
            password += random.choice(charset)
        
        # 打乱密码字符顺序
        password_list = list(password)
        random.shuffle(password_list)
        return ''.join(password_list)
    
    def evaluate_strength(self, password: str) -> Dict:
        """
        评估密码强度
        
        Args:
            password: 待评估的密码
            
        Returns:
            包含强度信息的字典
        """
        score = 0
        feedback = []
        
        # 长度评分
        if len(password) >= 16:
            score += 25
        elif len(password) >= 12:
            score += 20
        elif len(password) >= 8:
            score += 15
        else:
            score += 5
        
        # 字符类型多样性评分
        char_types = 0
        if re.search(r'[A-Z]', password):
            char_types += 1
        if re.search(r'[a-z]', password):
            char_types += 1
        if re.search(r'[0-9]', password):
            char_types += 1
        if re.search(r'[^A-Za-z0-9]', password):
            char_types += 1
        
        score += char_types * 15
        
        # 复杂度评分
        if len(password) >= 8 and char_types >= 3:
            score += 20
        if len(password) >= 12 and char_types >= 4:
            score += 20
        
        # 随机性评分（检查是否有重复模式）
        unique_chars = len(set(password))
        score += min(20, unique_chars * 2)
        
        # 确定强度等级
        if score >= 80:
            strength = "极强密码"
            color = "🟦"
        elif score >= 60:
            strength = "强密码"
            color = "🟩"
        elif score >= 40:
            strength = "中等密码"
            color = "🟨"
        else:
            strength = "弱密码"
            color = "🟥"
        
        return {
            'score': score,
            'strength': strength,
            'color': color,
            'feedback': feedback
        }
    
    def add_to_history(self, password: str, strength_info: Dict):
        """添加密码到历史记录"""
        history_item = {
            'password': password,
            'strength': strength_info['strength'],
            'score': strength_info['score'],
            'timestamp': self._get_timestamp()
        }
        self.password_history.insert(0, history_item)
        
        # 限制历史记录数量
        if len(self.password_history) > 20:
            self.password_history = self.password_history[:20]
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def display_history(self):
        """显示密码历史"""
        if not self.password_history:
            print("暂无密码历史记录")
            return
        
        print("\n📚 密码生成历史:")
        print("-" * 60)
        for i, item in enumerate(self.password_history, 1):
            print(f"{i:2d}. {item['password']}")
            print(f"    强度: {item['strength']} ({item['score']}分) | 时间: {item['timestamp']}")
            print()


def interactive_mode():
    """交互式模式"""
    generator = PasswordGenerator()
    
    print("🔐 随机密码生成器 - 交互模式")
    print("=" * 50)
    
    while True:
        try:
            print("\n请选择操作:")
            print("1. 生成单个密码")
            print("2. 批量生成密码")
            print("3. 查看密码历史")
            print("4. 清空密码历史")
            print("5. 退出")
            
            choice = input("\n请输入选择 (1-5): ").strip()
            
            if choice == '1':
                generate_single_password(generator)
            elif choice == '2':
                generate_multiple_passwords(generator)
            elif choice == '3':
                generator.display_history()
            elif choice == '4':
                if input("确定要清空所有密码历史记录吗？(y/N): ").lower() == 'y':
                    generator.password_history.clear()
                    print("密码历史已清空")
            elif choice == '5':
                print("感谢使用！再见！")
                break
            else:
                print("无效选择，请重新输入")
                
        except KeyboardInterrupt:
            print("\n\n程序被中断，再见！")
            break
        except Exception as e:
            print(f"发生错误: {e}")


def generate_single_password(generator: PasswordGenerator):
    """生成单个密码"""
    print("\n📋 密码配置:")
    
    # 获取密码长度
    while True:
        try:
            length = int(input("密码长度 (4-128): "))
            if 4 <= length <= 128:
                break
            else:
                print("长度必须在4-128之间")
        except ValueError:
            print("请输入有效的数字")
    
    # 获取字符类型选项
    print("\n选择字符类型:")
    use_uppercase = input("包含大写字母 (A-Z)? [Y/n]: ").lower() != 'n'
    use_lowercase = input("包含小写字母 (a-z)? [Y/n]: ").lower() != 'n'
    use_numbers = input("包含数字 (0-9)? [Y/n]: ").lower() != 'n'
    use_symbols = input("包含特殊符号 (!@#$%^&*)? [Y/n]: ").lower() != 'n'
    
    # 获取排除选项
    exclude_similar = input("排除相似字符 (0,O,1,I,l)? [y/N]: ").lower() == 'y'
    exclude_ambiguous = input("排除易混淆字符 ({},[],(),/,\\,|)? [y/N]: ").lower() == 'y'
    
    # 获取自定义字符
    custom_chars = input("自定义字符集 (可选): ").strip()
    
    # 生成密码
    options = {
        'use_uppercase': use_uppercase,
        'use_lowercase': use_lowercase,
        'use_numbers': use_numbers,
        'use_symbols': use_symbols,
        'exclude_similar': exclude_similar,
        'exclude_ambiguous': exclude_ambiguous,
        'custom_chars': custom_chars if custom_chars else None
    }
    
    try:
        password = generator.generate_password(length, options)
        strength_info = generator.evaluate_strength(password)
        
        # 显示结果
        print(f"\n🔑 生成的密码:")
        print(f"密码: {password}")
        print(f"强度: {strength_info['color']} {strength_info['strength']} ({strength_info['score']}分)")
        
        # 添加到历史记录
        generator.add_to_history(password, strength_info)
        
    except ValueError as e:
        print(f"生成失败: {e}")


def generate_multiple_passwords(generator: PasswordGenerator):
    """批量生成密码"""
    try:
        count = int(input("请输入要生成的密码数量 (1-10): "))
        if not 1 <= count <= 10:
            print("数量必须在1-10之间")
            return
    except ValueError:
        print("请输入有效的数字")
        return
    
    # 使用默认配置批量生成
    options = {
        'use_uppercase': True,
        'use_lowercase': True,
        'use_numbers': True,
        'use_symbols': True,
        'exclude_similar': False,
        'exclude_ambiguous': False,
        'custom_chars': None
    }
    
    print(f"\n📝 批量生成 {count} 个密码:")
    print("-" * 50)
    
    for i in range(count):
        try:
            password = generator.generate_password(16, options)
            strength_info = generator.evaluate_strength(password)
            print(f"{i+1:2d}. {password} - {strength_info['color']} {strength_info['strength']}")
            generator.add_to_history(password, strength_info)
        except ValueError as e:
            print(f"{i+1:2d}. 生成失败: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="随机密码生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s                    # 交互模式
  %(prog)s -l 16             # 生成16位密码
  %(prog)s -l 20 -n 5        # 生成5个20位密码
  %(prog)s -l 12 --no-symbols # 生成12位密码，不包含特殊符号
        """
    )
    
    parser.add_argument('-l', '--length', type=int, default=16,
                       help='密码长度 (默认: 16)')
    parser.add_argument('-n', '--number', type=int, default=1,
                       help='生成密码数量 (默认: 1)')
    parser.add_argument('--no-uppercase', action='store_true',
                       help='不包含大写字母')
    parser.add_argument('--no-lowercase', action='store_true',
                       help='不包含小写字母')
    parser.add_argument('--no-numbers', action='store_true',
                       help='不包含数字')
    parser.add_argument('--no-symbols', action='store_true',
                       help='不包含特殊符号')
    parser.add_argument('--exclude-similar', action='store_true',
                       help='排除相似字符 (0,O,1,I,l)')
    parser.add_argument('--exclude-ambiguous', action='store_true',
                       help='排除易混淆字符 ({},[],(),/,\\,|)')
    parser.add_argument('--custom-chars', type=str,
                       help='自定义字符集')
    parser.add_argument('--evaluate', type=str,
                       help='评估指定密码的强度')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='进入交互模式')
    
    args = parser.parse_args()
    
    # 如果指定了评估密码
    if args.evaluate:
        generator = PasswordGenerator()
        strength_info = generator.evaluate_strength(args.evaluate)
        print(f"密码: {args.evaluate}")
        print(f"强度: {strength_info['color']} {strength_info['strength']} ({strength_info['score']}分)")
        return
    
    # 如果指定了交互模式或没有其他参数
    if args.interactive or len(sys.argv) == 1:
        interactive_mode()
        return
    
    # 命令行模式
    generator = PasswordGenerator()
    
    options = {
        'use_uppercase': not args.no_uppercase,
        'use_lowercase': not args.no_lowercase,
        'use_numbers': not args.no_numbers,
        'use_symbols': not args.no_symbols,
        'exclude_similar': args.exclude_similar,
        'exclude_ambiguous': args.exclude_ambiguous,
        'custom_chars': args.custom_chars
    }
    
    try:
        for i in range(args.number):
            password = generator.generate_password(args.length, options)
            strength_info = generator.evaluate_strength(password)
            
            if args.number > 1:
                print(f"{i+1:2d}. {password}")
            else:
                print(f"密码: {password}")
                print(f"强度: {strength_info['color']} {strength_info['strength']} ({strength_info['score']}分)")
            
            generator.add_to_history(password, strength_info)
            
    except ValueError as e:
        print(f"生成失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()