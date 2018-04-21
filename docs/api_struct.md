- ###添加任务
    - #####描述
        将任务添加到任务队列
    - #####请求ULR:
        > POST  /scheduler

    - ####参数
        参数 | 必填 | 类型 | 说明
        ---|---|---|---
        trigger | Y | string | 任务触发器类型 interval\date\cron
        res_url | Y | string | 任务执行时的回调方法
        res_type | Y | string | 回调方法请求方式 get\post\delete\put
        job_name | Y | string | 任务名字 对应job_name
        job_id | N | string | 任务id 可不填, 不填的话系统会自动分配ID
        schedule_args | Y | json | 任务执行时间相关参数
        schedule_type| N | string | 任务类型 sys为系统任务 self为自定义任务 默认为self
        func_args| N | json | 回调方法相关参数
        user_id | N | string | 定义任务的用户ID, 0表示是系统任务
        remark | N | string | 任务备注      
        job_store | N | string | job_store 别名
        
    - ####请求示例
        ```json
        {
            "trigger": "cron",
            "res_url": "http://180.76.98.136/api/jx3/info",
            "res_type": "get",
            "job_name": "获取剑网三每日信息",
            "job_id": "get_jx3_info",
            "schedule_args": {
                "hour": 3
            },
            "schedule_type": "sys"
        }
        ```
        