@app.get("/routes")
async def list_all_routes():
    routes_list = []

    for route in app.routes:
        if isinstance(route, APIRoute) and not route.path.startswith(("/docs", "/redoc", "/openapi")):
            route_info = {
                "path": route.path,
                "name": route.name,
                "methods": list(route.methods),
                "endpoint": route.endpoint.__name__,
                "summary": route.summary,
            }
            routes_list.append(route_info)

    return routes_list
