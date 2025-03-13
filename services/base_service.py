class BaseService:
    async def transaction(self):
        """事务管理器"""
        return await db.transaction()

    def paginate(self, items, page, page_size):
        """通用分页方法"""
        pass 