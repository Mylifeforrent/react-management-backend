"""
响应工具模块
提供统一的API响应格式
"""

from flask import jsonify

def success_response(message="操作成功", data=None, code=200):
    """
    成功响应格式
    
    Args:
        message (str): 响应消息
        data (dict): 响应数据
        code (int): HTTP状态码
        
    Returns:
        Response: Flask响应对象
    """
    response_data = {
        "code": code,
        "message": message,
        "success": True
    }
    
    if data is not None:
        response_data["data"] = data
    
    return jsonify(response_data), code

def error_response(message="操作失败", data=None, code=400):
    """
    错误响应格式
    
    Args:
        message (str): 错误消息
        data (dict): 错误详情数据
        code (int): HTTP状态码
        
    Returns:
        Response: Flask响应对象
    """
    response_data = {
        "code": code,
        "message": message,
        "success": False
    }
    
    if data is not None:
        response_data["data"] = data
    
    return jsonify(response_data), code

def paginated_response(items, pagination, message="获取数据成功"):
    """
    分页响应格式
    
    Args:
        items (list): 数据列表
        pagination: SQLAlchemy分页对象
        message (str): 响应消息
        
    Returns:
        Response: Flask响应对象
    """
    return success_response(
        message=message,
        data={
            "items": items,
            "pagination": {
                "page": pagination.page,
                "pages": pagination.pages,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev,
                "next_num": pagination.next_num,
                "prev_num": pagination.prev_num
            }
        }
    )

def validation_error_response(errors):
    """
    数据验证错误响应
    
    Args:
        errors (dict): 验证错误详情
        
    Returns:
        Response: Flask响应对象
    """
    return error_response(
        message="数据验证失败",
        data={"validation_errors": errors},
        code=422
    )

def not_found_response(resource="资源"):
    """
    资源不存在响应
    
    Args:
        resource (str): 资源名称
        
    Returns:
        Response: Flask响应对象
    """
    return error_response(
        message=f"{resource}不存在",
        code=404
    )

def unauthorized_response(message="未授权访问"):
    """
    未授权响应
    
    Args:
        message (str): 错误消息
        
    Returns:
        Response: Flask响应对象
    """
    return error_response(
        message=message,
        code=401
    )

def forbidden_response(message="权限不足"):
    """
    权限不足响应
    
    Args:
        message (str): 错误消息
        
    Returns:
        Response: Flask响应对象
    """
    return error_response(
        message=message,
        code=403
    )

def server_error_response(message="服务器内部错误"):
    """
    服务器错误响应
    
    Args:
        message (str): 错误消息
        
    Returns:
        Response: Flask响应对象
    """
    return error_response(
        message=message,
        code=500
    )