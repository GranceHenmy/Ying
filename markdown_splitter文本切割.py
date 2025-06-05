import os
from typing import List

def split_markdown_by_chars(md_text: str, chunk_size: int = 5000) -> List[str]:
    """
    按固定字符数分割Markdown文本
    :param md_text: 输入的Markdown文本
    :param chunk_size: 每个块的字符数，默认1000
    :return: 分割后的文本块列表
    """
    chunks = []
    current_chunk = []
    current_length = 0
    
    # 按段落分割后再按字符数处理
    paragraphs = md_text.split('\n\n')
    
    for para in paragraphs:
        para_length = len(para)
        
        # 如果当前段落会使块超过大小限制
        if current_length + para_length > chunk_size and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = []
            current_length = 0
            
        current_chunk.append(para)
        current_length += para_length + 2  # 加上两个换行符的长度
    
    # 添加最后一个块
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks

def process_markdown_file(input_path: str, output_dir: str, chunk_size: int = 1000):
    """
    处理Markdown文件并输出分割后的块
    :param input_path: 输入文件路径
    :param output_dir: 输出目录
    :param chunk_size: 每个块的字符数
    """
    # 读取文件内容
    with open(input_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    # 获取基础文件名（不带扩展名）
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    
    # 分割文本
    chunks = split_markdown_by_chars(md_text, chunk_size)
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存分割后的块
    for i, chunk in enumerate(chunks):
        output_path = os.path.join(output_dir, f'{base_name}-part-{i+1}.md')  # 修改文件名格式
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(chunk)
    
    print(f"文件已分割为 {len(chunks)} 个块，保存在 {output_dir}")

if __name__ == "__main__":
    # 示例用法
    input_file = "E:\\00.Dify平台-知识库文档\\00.公司制度文件\\00.远东股份-制度\\00.远东股份-人力资源制度\\06.2025年5月版本\\人力资源制度.md"
    output_dir = "E:\\00.Dify平台-知识库文档\\01.人力资源制度分块"
    
    # 处理文件前设置控制台编码
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    process_markdown_file(input_file, output_dir, 4500)  # 每块500字符