# -*- coding: utf-8 -*-
import joblib
import argparse
import os

def pkl2txt(pkl_file, output_txt_file):
    # 加载pkl文件
    data = joblib.load(pkl_file)
    
    # 将数据转换为字符串格式
    data_str = str(data)
    
    # 将数据写入txt文件
    with open(output_txt_file, 'w') as f:
        f.write(data_str)
    
    print(f"Data from {pkl_file} has been saved to {output_txt_file}")

def visualize_data(data):
    # 可视化展示数据（这里只是简单的打印数据）
    print("Visualizing data:")
    print(data)

def main():
    parser = argparse.ArgumentParser(description="Convert pkl file to txt and visualize data")
    parser.add_argument('pkl_file', type=str, help='Path to the input pkl file')
    parser.add_argument('output_txt_file', type=str, help='Path to the output txt file')
    
    args = parser.parse_args()
    
    # 读取并转换数据
    data = joblib.load(args.pkl_file)
    pkl2txt(args.pkl_file, args.output_txt_file)
    
    # 可视化数据
    visualize_data(data)

if __name__ == "__main__":
    main()
