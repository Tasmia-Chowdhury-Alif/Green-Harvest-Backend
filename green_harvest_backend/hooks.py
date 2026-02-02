

def custom_tag_generator(result, generator, request, public):
    """
    Assign 'auth' and 'products' tags based on path prefixes.
    This groups Djoser endpoints under 'auth' and your app under 'products'.
    """
    for path, path_item in result['paths'].items():
        if path.startswith('/api/auth/'):
            for operation in path_item.values():
                operation['tags'] = ['auth']
        elif path.startswith('/api/products/') or path.startswith('/api/categories/'):
            for operation in path_item.values():
                operation['tags'] = ['products']
    return result