#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
密码生成器演示脚本
展示各种功能和用法
"""

from password_generator import PasswordGenerator
import time

def demo_basic_generation():
    """演示基本密码生成"""
    print("🎯 基本密码生成演示")
    print("-" * 40)
    
    generator = PasswordGenerator()
    
    # 生成不同长度的密码
    lengths = [8, 12, 16, 20]
    for length in lengths:
        password = generator.generate_password(length, {
            'use_uppercase': True,
            'use_lowercase': True,
            'use_numbers': True,
            'use_symbols': True,
            'exclude_similar': False,
            'exclude_ambiguous': False,
            'custom_chars': None
        })
        strength = generator.evaluate_strength(password)
        print(f"{length:2d}位: {password} - {strength['color']} {strength['strength']} ({strength['score']}分)")
    
    print()

def demo_character_options():
    """演示字符类型选项"""
    print("🔤 字符类型选项演示")
    print("-" * 40)
    
    generator = PasswordGenerator()
    
    options_list = [
        ("仅大写字母", {'use_uppercase': True, 'use_lowercase': False, 'use_numbers': False, 'use_symbols': False}),
        ("仅小写字母", {'use_uppercase': False, 'use_lowercase': True, 'use_numbers': False, 'use_symbols': False}),
        ("仅数字", {'use_uppercase': False, 'use_lowercase': False, 'use_numbers': True, 'use_symbols': False}),
        ("仅特殊符号", {'use_uppercase': False, 'use_lowercase': False, 'use_numbers': False, 'use_symbols': True}),
        ("字母+数字", {'use_uppercase': True, 'use_lowercase': True, 'use_numbers': True, 'use_symbols': False}),
        ("字母+符号", {'use_uppercase': True, 'use_lowercase': True, 'use_numbers': False, 'use_symbols': True}),
    ]
    
    for name, options in options_list:
        options.update({
            'exclude_similar': False,
            'exclude_ambiguous': False,
            'custom_chars': None
        })
        
        password = generator.generate_password(12, options)
        strength = generator.evaluate_strength(password)
        print(f"{name:12s}: {password} - {strength['color']} {strength['strength']}")
    
    print()

def demo_exclusion_options():
    """演示排除选项"""
    print("🚫 排除选项演示")
    print("-" * 40)
    
    generator = PasswordGenerator()
    
    # 标准密码
    standard_password = generator.generate_password(16, {
        'use_uppercase': True,
        'use_lowercase': True,
        'use_numbers': True,
        'use_symbols': True,
        'exclude_similar': False,
        'exclude_ambiguous': False,
        'custom_chars': None
    })
    
    # 排除相似字符
    no_similar = generator.generate_password(16, {
        'use_uppercase': True,
        'use_lowercase': True,
        'use_numbers': True,
        'use_symbols': True,
        'exclude_similar': True,
        'exclude_ambiguous': False,
        'custom_chars': None
    })
    
    # 排除易混淆字符
    no_ambiguous = generator.generate_password(16, {
        'use_uppercase': True,
        'use_lowercase': True,
        'use_numbers': True,
        'use_symbols': True,
        'exclude_similar': False,
        'exclude_ambiguous': True,
        'custom_chars': None
    })
    
    print(f"标准密码:     {standard_password}")
    print(f"排除相似字符: {no_similar}")
    print(f"排除易混淆:   {no_ambiguous}")
    print()

def demo_custom_characters():
    """演示自定义字符集"""
    print("🎨 自定义字符集演示")
    print("-" * 40)
    
    generator = PasswordGenerator()
    
    custom_sets = [
        ("中文", "中文密码生成器"),
        ("Emoji", "🚀🎉💻🔐✨"),
        ("希腊字母", "αβγδεζηθικλμνξοπρστυφχψω"),
        ("数学符号", "∑∏∫√∞≠≤≥±×÷"),
        ("中英混合", "中文English123🚀")
    ]
    
    for name, chars in custom_sets:
        password = generator.generate_password(10, {
            'use_uppercase': False,
            'use_lowercase': False,
            'use_numbers': False,
            'use_symbols': False,
            'exclude_similar': False,
            'exclude_ambiguous': False,
            'custom_chars': chars
        })
        print(f"{name:8s}: {password}")
    
    print()

def demo_strength_evaluation():
    """演示密码强度评估"""
    print("📊 密码强度评估演示")
    print("-" * 40)
    
    generator = PasswordGenerator()
    
    test_passwords = [
        "123",
        "password",
        "Password",
        "Password123",
        "P@ssw0rd123!",
        "MyV3ryS3cur3P@ssw0rd!",
        "这是一个中文密码123！🚀",
        "a" * 50,  # 重复字符
        "abcdefghijklmnopqrstuvwxyz",  # 连续字母
        "qwertyuiop",  # 键盘序列
    ]
    
    for password in test_passwords:
        strength = generator.evaluate_strength(password)
        print(f"{password[:20]:20s} - {strength['color']} {strength['strength']:8s} ({strength['score']:3d}分)")
    
    print()

def demo_batch_generation():
    """演示批量生成"""
    print("📝 批量生成演示")
    print("-" * 40)
    
    generator = PasswordGenerator()
    
    # 生成不同类型的密码
    batch_options = [
        ("强密码", {'use_uppercase': True, 'use_lowercase': True, 'use_numbers': True, 'use_symbols': True}),
        ("纯数字", {'use_uppercase': False, 'use_lowercase': False, 'use_numbers': True, 'use_symbols': False}),
        ("纯字母", {'use_uppercase': True, 'use_lowercase': True, 'use_numbers': False, 'use_symbols': False}),
    ]
    
    for name, options in batch_options:
        options.update({
            'exclude_similar': False,
            'exclude_ambiguous': False,
            'custom_chars': None
        })
        
        print(f"{name}:")
        for i in range(3):
            password = generator.generate_password(12, options)
            strength = generator.evaluate_strength(password)
            print(f"  {i+1}. {password} - {strength['color']} {strength['strength']}")
        print()

def demo_performance():
    """演示性能测试"""
    print("⚡ 性能测试演示")
    print("-" * 40)
    
    generator = PasswordGenerator()
    
    # 测试生成速度
    start_time = time.time()
    count = 1000
    
    for _ in range(count):
        generator.generate_password(16, {
            'use_uppercase': True,
            'use_lowercase': True,
            'use_numbers': True,
            'use_symbols': True,
            'exclude_similar': False,
            'exclude_ambiguous': False,
            'custom_chars': None
        })
    
    end_time = time.time()
    elapsed = end_time - start_time
    rate = count / elapsed
    
    print(f"生成 {count} 个16位密码耗时: {elapsed:.3f}秒")
    print(f"平均速度: {rate:.0f} 密码/秒")
    print()

def main():
    """主演示函数"""
    print("🔐 随机密码生成器 - 功能演示")
    print("=" * 60)
    
    demos = [
        demo_basic_generation,
        demo_character_options,
        demo_exclusion_options,
        demo_custom_characters,
        demo_strength_evaluation,
        demo_batch_generation,
        demo_performance
    ]
    
    for demo in demos:
        try:
            demo()
            time.sleep(0.5)  # 稍微暂停，让输出更清晰
        except Exception as e:
            print(f"演示 {demo.__name__} 时发生错误: {e}")
            print()
    
    print("🎉 演示完成！")
    print("\n💡 提示:")
    print("- 使用 python3 password_generator.py 进入交互模式")
    print("- 使用 python3 password_generator.py --help 查看命令行选项")
    print("- 打开 password-generator.html 使用Web界面")

if __name__ == "__main__":
    main()