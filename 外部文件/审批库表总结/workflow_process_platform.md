# workflow_process_platform 数据库表结构文档

## 数据库概述
- 数据库名称：workflow_process_platform
- 数据库用途：基于Activiti工作流引擎的流程平台系统
- 表总数：33张（25张Activiti标准表 + 8张业务扩展表）

## 数据库架构说明

`workflow_process_platform` 数据库包含两大类表：

### 1. Activiti标准表（以 `act_` 开头）
这些是Activiti工作流引擎的标准系统表，用于存储流程定义、流程实例、任务、历史记录等核心数据：
- **通用表（GE）**: 存储引擎通用数据如二进制资源、系统属性
- **仓库表（RE）**: 存储流程定义、部署、模型等静态资源
- **运行时表（RU）**: 存储当前运行中的流程实例、任务、变量等
- **历史表（HI）**: 存储已完成的流程、任务、变量等历史数据

### 2. 业务扩展表（以 `workflow_process_` 开头）
这些是针对业务需求定制开发的扩展表，用于存储流程节点配置、代理任务等业务相关数据。

## Activiti系统表详情

### act_evt_log
**业务含义**: Activiti引擎的事件日志记录表，存储引擎执行过程中的各种事件信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| LOG_NR_ | bigint(20) | NO | PRI | | 日志编号，自增主键 |
| TYPE_ | varchar(64) | YES | | | 事件类型 |
| PROC_DEF_ID_ | varchar(64) | YES | | | 流程定义ID |
| PROC_INST_ID_ | varchar(64) | YES | | | 流程实例ID |
| EXECUTION_ID_ | varchar(64) | YES | | | 执行实例ID |
| TASK_ID_ | varchar(64) | YES | | | 任务ID |
| TIME_STAMP_ | timestamp(3) | NO | | CURRENT_TIMESTAMP(3) | 时间戳 |
| USER_ID_ | varchar(255) | YES | | | 用户ID |
| DATA_ | longblob | YES | | | 事件数据 |
| LOCK_OWNER_ | varchar(255) | YES | | | 锁拥有者 |
| LOCK_TIME_ | timestamp(3) | YES | | | 锁定时间 |
| IS_PROCESSED_ | tinyint(4) | YES | | 0 | 是否已处理 |

### act_ge_bytearray
**业务含义**: Activiti通用二进制资源存储表，用于存储部署资源文件、流程图等二进制数据

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| REV_ | int(11) | YES | | | 版本号 |
| NAME_ | varchar(255) | YES | | | 资源名称 |
| DEPLOYMENT_ID_ | varchar(64) | YES | MUL | | 部署ID，多重索引 |
| BYTES_ | longblob | YES | | | 二进制数据 |
| GENERATED_ | tinyint(4) | YES | | | 是否自动生成 |

### act_ge_property
**业务含义**: Activiti引擎系统属性配置表，存储引擎版本、数据库版本等系统级配置

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| NAME_ | varchar(64) | NO | PRI | | 属性名称，主键 |
| VALUE_ | varchar(300) | YES | | | 属性值 |
| REV_ | int(11) | YES | | | 版本号 |

### act_hi_actinst
**业务含义**: Activiti历史活动实例表，记录流程中每个活动节点的历史执行信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| PROC_DEF_ID_ | varchar(64) | NO | | | 流程定义ID |
| PROC_INST_ID_ | varchar(64) | NO | MUL | | 流程实例ID，多重索引 |
| EXECUTION_ID_ | varchar(64) | NO | MUL | | 执行实例ID，多重索引 |
| ACT_ID_ | varchar(255) | NO | | | 活动ID |
| TASK_ID_ | varchar(64) | YES | | | 任务ID |
| CALL_PROC_INST_ID_ | varchar(64) | YES | | | 调用的流程实例ID |
| ACT_NAME_ | varchar(255) | YES | | | 活动名称 |
| ACT_TYPE_ | varchar(255) | NO | | | 活动类型 |
| ASSIGNEE_ | varchar(255) | YES | | | 执行人 |
| START_TIME_ | datetime(3) | NO | MUL | | 开始时间，多重索引 |
| END_TIME_ | datetime(3) | YES | MUL | | 结束时间，多重索引 |
| DURATION_ | bigint(20) | YES | | | 持续时间 |
| DELETE_REASON_ | varchar(4000) | YES | | | 删除原因 |
| TENANT_ID_ | varchar(255) | YES | | "" | 租户ID |

### act_hi_attachment
**业务含义**: Activiti历史附件表，记录流程或任务相关的附件信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| REV_ | int(11) | YES | | | 版本号 |
| USER_ID_ | varchar(255) | YES | | | 用户ID |
| NAME_ | varchar(255) | YES | | | 附件名称 |
| DESCRIPTION_ | varchar(4000) | YES | | | 附件描述 |
| TYPE_ | varchar(255) | YES | | | 附件类型 |
| TASK_ID_ | varchar(64) | YES | | | 任务ID |
| PROC_INST_ID_ | varchar(64) | YES | | | 流程实例ID |
| URL_ | varchar(4000) | YES | | | 附件URL |
| CONTENT_ID_ | varchar(64) | YES | | | 内容ID |
| TIME_ | datetime(3) | YES | | | 创建时间 |

### act_hi_comment
**业务含义**: Activiti历史评论表，记录流程或任务的评论信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| TYPE_ | varchar(255) | YES | | | 评论类型 |
| TIME_ | datetime(3) | NO | | | 评论时间 |
| USER_ID_ | varchar(255) | YES | | | 评论用户ID |
| TASK_ID_ | varchar(64) | YES | | | 任务ID |
| PROC_INST_ID_ | varchar(64) | YES | MUL | | 流程实例ID，多重索引 |
| ACTION_ | varchar(255) | YES | | | 动作类型 |
| MESSAGE_ | varchar(4000) | YES | | | 评论消息 |
| FULL_MSG_ | longblob | YES | | | 完整消息 |

### act_hi_detail
**业务含义**: Activiti历史变量详细信息表，记录流程变量的历史变更详情

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| TYPE_ | varchar(255) | NO | | | 变量类型 |
| PROC_INST_ID_ | varchar(64) | YES | MUL | | 流程实例ID，多重索引 |
| EXECUTION_ID_ | varchar(64) | YES | | | 执行实例ID |
| TASK_ID_ | varchar(64) | YES | MUL | | 任务ID，多重索引 |
| ACT_INST_ID_ | varchar(64) | YES | MUL | | 活动实例ID，多重索引 |
| NAME_ | varchar(255) | NO | MUL | | 变量名称，多重索引 |
| VAR_TYPE_ | varchar(255) | YES | | | 变量数据类型 |
| REV_ | int(11) | YES | | | 版本号 |
| TIME_ | datetime(3) | NO | MUL | | 时间，多重索引 |
| BYTEARRAY_ID_ | varchar(64) | YES | | | 二进制数组ID |
| DOUBLE_ | double | YES | | | 双精度值 |
| LONG_ | bigint(20) | YES | | | 长整型值 |
| TEXT_ | varchar(4000) | YES | | | 文本值 |
| TEXT2_ | varchar(4000) | YES | | | 文本值2 |

### act_hi_identitylink
**业务含义**: Activiti历史身份关联表，记录用户与任务、流程的历史关联关系

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| GROUP_ID_ | varchar(255) | YES | | | 组ID |
| TYPE_ | varchar(255) | YES | | | 关联类型 |
| USER_ID_ | varchar(255) | YES | MUL | | 用户ID，多重索引 |
| TASK_ID_ | varchar(64) | YES | MUL | | 任务ID，多重索引 |
| PROC_INST_ID_ | varchar(64) | YES | MUL | | 流程实例ID，多重索引 |

### act_hi_procinst
**业务含义**: Activiti历史流程实例表，记录已完成或删除的流程实例信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| PROC_INST_ID_ | varchar(64) | NO | UNI | | 流程实例ID，唯一索引 |
| BUSINESS_KEY_ | varchar(255) | YES | MUL | | 业务主键，多重索引 |
| PROC_DEF_ID_ | varchar(64) | NO | | | 流程定义ID |
| START_TIME_ | datetime(3) | NO | | | 开始时间 |
| END_TIME_ | datetime(3) | YES | MUL | | 结束时间，多重索引 |
| DURATION_ | bigint(20) | YES | | | 持续时间 |
| START_USER_ID_ | varchar(255) | YES | | | 发起用户ID |
| START_ACT_ID_ | varchar(255) | YES | | | 开始活动ID |
| END_ACT_ID_ | varchar(255) | YES | | | 结束活动ID |
| SUPER_PROCESS_INSTANCE_ID_ | varchar(64) | YES | | | 父流程实例ID |
| DELETE_REASON_ | varchar(4000) | YES | | | 删除原因 |
| TENANT_ID_ | varchar(255) | YES | | "" | 租户ID |
| NAME_ | varchar(255) | YES | | | 流程实例名称 |

### act_hi_taskinst
**业务含义**: Activiti历史任务实例表，记录已完成或删除的任务实例信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| PROC_DEF_ID_ | varchar(64) | YES | | | 流程定义ID |
| TASK_DEF_KEY_ | varchar(255) | YES | | | 任务定义Key |
| PROC_INST_ID_ | varchar(64) | YES | MUL | | 流程实例ID，多重索引 |
| EXECUTION_ID_ | varchar(64) | YES | | | 执行实例ID |
| NAME_ | varchar(255) | YES | | | 任务名称 |
| PARENT_TASK_ID_ | varchar(64) | YES | MUL | | 父任务ID，多重索引 |
| DESCRIPTION_ | varchar(4000) | YES | | | 任务描述 |
| OWNER_ | varchar(255) | YES | | | 任务拥有者 |
| ASSIGNEE_ | varchar(255) | YES | | | 任务执行人 |
| START_TIME_ | datetime(3) | NO | | | 开始时间 |
| CLAIM_TIME_ | datetime(3) | YES | | | 领取时间 |
| END_TIME_ | datetime(3) | YES | | | 结束时间 |
| DURATION_ | bigint(20) | YES | | | 持续时间 |
| DELETE_REASON_ | varchar(4000) | YES | | | 删除原因 |
| PRIORITY_ | int(11) | YES | | | 优先级 |
| DUE_DATE_ | datetime(3) | YES | | | 到期时间 |
| FORM_KEY_ | varchar(255) | YES | | | 表单Key |
| CATEGORY_ | varchar(255) | YES | | | 任务分类 |
| TENANT_ID_ | varchar(255) | YES | | "" | 租户ID |

### act_hi_varinst
**业务含义**: Activiti历史变量实例表，记录流程变量的历史值信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| PROC_INST_ID_ | varchar(64) | YES | MUL | | 流程实例ID，多重索引 |
| EXECUTION_ID_ | varchar(64) | YES | MUL | | 执行实例ID，多重索引 |
| TASK_ID_ | varchar(64) | YES | MUL | | 任务ID，多重索引 |
| NAME_ | varchar(255) | NO | MUL | | 变量名称，多重索引 |
| VAR_TYPE_ | varchar(100) | YES | | | 变量类型 |
| REV_ | int(11) | YES | | | 版本号 |
| BYTEARRAY_ID_ | varchar(64) | YES | | | 二进制数组ID |
| DOUBLE_ | double | YES | | | 双精度值 |
| LONG_ | bigint(20) | YES | | | 长整型值 |
| TEXT_ | varchar(4000) | YES | | | 文本值 |
| TEXT2_ | varchar(4000) | YES | | | 文本值2 |
| CREATE_TIME_ | datetime(3) | YES | | | 创建时间 |
| LAST_UPDATED_TIME_ | datetime(3) | YES | | | 最后更新时间 |

### act_procdef_info
**业务含义**: Activiti流程定义扩展信息表，存储流程定义的附加信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| PROC_DEF_ID_ | varchar(64) | NO | UNI | | 流程定义ID，唯一索引 |
| REV_ | int(11) | YES | | | 版本号 |
| INFO_JSON_ID_ | varchar(64) | YES | MUL | | JSON信息ID，多重索引 |

### act_re_deployment
**业务含义**: Activiti流程部署表，记录流程定义的部署信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| NAME_ | varchar(255) | YES | | | 部署名称 |
| CATEGORY_ | varchar(255) | YES | | | 部署分类 |
| KEY_ | varchar(255) | YES | | | 部署Key |
| TENANT_ID_ | varchar(255) | YES | | "" | 租户ID |
| DEPLOY_TIME_ | timestamp(3) | YES | | | 部署时间 |
| ENGINE_VERSION_ | varchar(255) | YES | | | 引擎版本 |
| VERSION_ | int(11) | YES | | 1 | 版本号 |
| PROJECT_RELEASE_VERSION_ | varchar(255) | YES | | | 项目发布版本 |

### act_re_model
**业务含义**: Activiti流程模型表，存储流程设计器创建的模型信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| REV_ | int(11) | YES | | | 版本号 |
| NAME_ | varchar(255) | YES | | | 模型名称 |
| KEY_ | varchar(255) | YES | | | 模型Key |
| CATEGORY_ | varchar(255) | YES | | | 模型分类 |
| CREATE_TIME_ | timestamp(3) | YES | | | 创建时间 |
| LAST_UPDATE_TIME_ | timestamp(3) | YES | | | 最后更新时间 |
| VERSION_ | int(11) | YES | | | 版本号 |
| META_INFO_ | varchar(4000) | YES | | | 元信息 |
| DEPLOYMENT_ID_ | varchar(64) | YES | MUL | | 部署ID，多重索引 |
| EDITOR_SOURCE_VALUE_ID_ | varchar(64) | YES | MUL | | 编辑器源值ID，多重索引 |
| EDITOR_SOURCE_EXTRA_VALUE_ID_ | varchar(64) | YES | MUL | | 编辑器源额外值ID，多重索引 |
| TENANT_ID_ | varchar(255) | YES | | "" | 租户ID |

### act_re_procdef
**业务含义**: Activiti流程定义表，存储已部署的流程定义信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| REV_ | int(11) | YES | | | 版本号 |
| CATEGORY_ | varchar(255) | YES | | | 流程分类 |
| NAME_ | varchar(255) | YES | | | 流程名称 |
| KEY_ | varchar(255) | NO | MUL | | 流程Key，多重索引 |
| VERSION_ | int(11) | NO | | | 流程版本 |
| DEPLOYMENT_ID_ | varchar(64) | YES | | | 部署ID |
| RESOURCE_NAME_ | varchar(4000) | YES | | | 资源名称 |
| DGRM_RESOURCE_NAME_ | varchar(4000) | YES | | | 流程图资源名称 |
| DESCRIPTION_ | varchar(4000) | YES | | | 流程描述 |
| HAS_START_FORM_KEY_ | tinyint(4) | YES | | | 是否有启动表单 |
| HAS_GRAPHICAL_NOTATION_ | tinyint(4) | YES | | | 是否有图形表示 |
| SUSPENSION_STATE_ | int(11) | YES | | | 挂起状态 |
| TENANT_ID_ | varchar(255) | YES | | "" | 租户ID |
| ENGINE_VERSION_ | varchar(255) | YES | | | 引擎版本 |
| APP_VERSION_ | int(11) | YES | | | 应用版本 |

### act_ru_deadletter_job
**业务含义**: Activiti死信任务表，存储执行失败且重试次数耗尽的任务

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| REV_ | int(11) | YES | | | 版本号 |
| TYPE_ | varchar(255) | NO | | | 任务类型 |
| EXCLUSIVE_ | tinyint(1) | YES | | | 是否独占 |
| EXECUTION_ID_ | varchar(64) | YES | MUL | | 执行实例ID，多重索引 |
| PROCESS_INSTANCE_ID_ | varchar(64) | YES | MUL | | 流程实例ID，多重索引 |
| PROC_DEF_ID_ | varchar(64) | YES | MUL | | 流程定义ID，多重索引 |
| EXCEPTION_STACK_ID_ | varchar(64) | YES | MUL | | 异常堆栈ID，多重索引 |
| EXCEPTION_MSG_ | varchar(4000) | YES | | | 异常信息 |
| DUEDATE_ | timestamp(3) | YES | | | 到期时间 |
| REPEAT_ | varchar(255) | YES | | | 重复配置 |
| HANDLER_TYPE_ | varchar(255) | YES | | | 处理器类型 |
| HANDLER_CFG_ | varchar(4000) | YES | | | 处理器配置 |
| TENANT_ID_ | varchar(255) | YES | | "" | 租户ID |

### act_ru_event_subscr
**业务含义**: Activiti事件订阅表，存储流程中的事件订阅信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| REV_ | int(11) | YES | | | 版本号 |
| EVENT_TYPE_ | varchar(255) | NO | | | 事件类型 |
| EVENT_NAME_ | varchar(255) | YES | | | 事件名称 |
| EXECUTION_ID_ | varchar(64) | YES | MUL | | 执行实例ID，多重索引 |
| PROC_INST_ID_ | varchar(64) | YES | | | 流程实例ID |
| ACTIVITY_ID_ | varchar(64) | YES | | | 活动ID |
| CONFIGURATION_ | varchar(255) | YES | MUL | | 配置信息，多重索引 |
| CREATED_ | timestamp(3) | NO | | CURRENT_TIMESTAMP(3) | 创建时间 |
| PROC_DEF_ID_ | varchar(64) | YES | | | 流程定义ID |
| TENANT_ID_ | varchar(255) | YES | | "" | 租户ID |

### act_ru_execution
**业务含义**: Activiti运行时执行实例表，存储当前正在运行的流程执行信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| REV_ | int(11) | YES | | | 版本号 |
| PROC_INST_ID_ | varchar(64) | YES | MUL | | 流程实例ID，多重索引 |
| BUSINESS_KEY_ | varchar(255) | YES | MUL | | 业务主键，多重索引 |
| PARENT_ID_ | varchar(64) | YES | MUL | | 父执行ID，多重索引 |
| PROC_DEF_ID_ | varchar(64) | YES | MUL | | 流程定义ID，多重索引 |
| SUPER_EXEC_ | varchar(64) | YES | MUL | | 上级执行ID，多重索引 |
| ROOT_PROC_INST_ID_ | varchar(64) | YES | MUL | | 根流程实例ID，多重索引 |
| ACT_ID_ | varchar(255) | YES | | | 活动ID |
| IS_ACTIVE_ | tinyint(4) | YES | | | 是否活跃 |
| IS_CONCURRENT_ | tinyint(4) | YES | | | 是否并发 |
| IS_SCOPE_ | tinyint(4) | YES | | | 是否作用域 |
| IS_EVENT_SCOPE_ | tinyint(4) | YES | | | 是否事件作用域 |
| IS_MI_ROOT_ | tinyint(4) | YES | | | 是否多实例根 |
| SUSPENSION_STATE_ | int(11) | YES | | | 挂起状态 |
| CACHED_ENT_STATE_ | int(11) | YES | | | 缓存实体状态 |
| TENANT_ID_ | varchar(255) | YES | | "" | 租户ID |
| NAME_ | varchar(255) | YES | | | 执行名称 |
| START_TIME_ | datetime(3) | YES | | | 开始时间 |
| START_USER_ID_ | varchar(255) | YES | | | 启动用户ID |
| LOCK_TIME_ | timestamp(3) | YES | | | 锁定时间 |
| IS_COUNT_ENABLED_ | tinyint(4) | YES | | | 是否启用计数 |
| EVT_SUBSCR_COUNT_ | int(11) | YES | | | 事件订阅计数 |
| TASK_COUNT_ | int(11) | YES | | | 任务计数 |
| JOB_COUNT_ | int(11) | YES | | | 任务计数 |
| TIMER_JOB_COUNT_ | int(11) | YES | | | 定时任务计数 |
| SUSP_JOB_COUNT_ | int(11) | YES | | | 挂起任务计数 |
| DEADLETTER_JOB_COUNT_ | int(11) | YES | | | 死信任务计数 |
| VAR_COUNT_ | int(11) | YES | | | 变量计数 |
| ID_LINK_COUNT_ | int(11) | YES | | | 身份链接计数 |
| APP_VERSION_ | int(11) | YES | | | 应用版本 |

### act_ru_identitylink
**业务含义**: Activiti运行时身份关联表，存储当前任务与用户、组的关联关系

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| REV_ | int(11) | YES | | | 版本号 |
| GROUP_ID_ | varchar(255) | YES | MUL | | 组ID，多重索引 |
| TYPE_ | varchar(255) | YES | | | 关联类型 |
| USER_ID_ | varchar(255) | YES | MUL | | 用户ID，多重索引 |
| TASK_ID_ | varchar(64) | YES | MUL | | 任务ID，多重索引 |
| PROC_INST_ID_ | varchar(64) | YES | MUL | | 流程实例ID，多重索引 |
| PROC_DEF_ID_ | varchar(64) | YES | MUL | | 流程定义ID，多重索引 |

### act_ru_integration
**业务含义**: Activiti运行时集成表，用于记录与外部系统的集成信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| EXECUTION_ID_ | varchar(64) | YES | MUL | | 执行实例ID，多重索引 |
| PROCESS_INSTANCE_ID_ | varchar(64) | YES | MUL | | 流程实例ID，多重索引 |
| PROC_DEF_ID_ | varchar(64) | YES | MUL | | 流程定义ID，多重索引 |
| FLOW_NODE_ID_ | varchar(64) | YES | | | 流程节点ID |
| CREATED_DATE_ | timestamp(3) | NO | | CURRENT_TIMESTAMP(3) | 创建时间 |

### act_ru_job
**业务含义**: Activiti运行时任务表，存储当前需要执行的异步任务

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| REV_ | int(11) | YES | | | 版本号 |
| TYPE_ | varchar(255) | NO | | | 任务类型 |
| LOCK_EXP_TIME_ | timestamp(3) | YES | | | 锁过期时间 |
| LOCK_OWNER_ | varchar(255) | YES | | | 锁拥有者 |
| EXCLUSIVE_ | tinyint(1) | YES | | | 是否独占 |
| EXECUTION_ID_ | varchar(64) | YES | MUL | | 执行实例ID，多重索引 |
| PROCESS_INSTANCE_ID_ | varchar(64) | YES | MUL | | 流程实例ID，多重索引 |
| PROC_DEF_ID_ | varchar(64) | YES | MUL | | 流程定义ID，多重索引 |
| RETRIES_ | int(11) | YES | | | 重试次数 |
| EXCEPTION_STACK_ID_ | varchar(64) | YES | MUL | | 异常堆栈ID，多重索引 |
| EXCEPTION_MSG_ | varchar(4000) | YES | | | 异常信息 |
| DUEDATE_ | timestamp(3) | YES | | | 到期时间 |
| REPEAT_ | varchar(255) | YES | | | 重复配置 |
| HANDLER_TYPE_ | varchar(255) | YES | | | 处理器类型 |
| HANDLER_CFG_ | varchar(4000) | YES | | | 处理器配置 |
| TENANT_ID_ | varchar(255) | YES | | "" | 租户ID |

### act_ru_suspended_job
**业务含义**: Activiti挂起任务表，存储被挂起的异步任务

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| REV_ | int(11) | YES | | | 版本号 |
| TYPE_ | varchar(255) | NO | | | 任务类型 |
| EXCLUSIVE_ | tinyint(1) | YES | | | 是否独占 |
| EXECUTION_ID_ | varchar(64) | YES | MUL | | 执行实例ID，多重索引 |
| PROCESS_INSTANCE_ID_ | varchar(64) | YES | MUL | | 流程实例ID，多重索引 |
| PROC_DEF_ID_ | varchar(64) | YES | MUL | | 流程定义ID，多重索引 |
| RETRIES_ | int(11) | YES | | | 重试次数 |
| EXCEPTION_STACK_ID_ | varchar(64) | YES | MUL | | 异常堆栈ID，多重索引 |
| EXCEPTION_MSG_ | varchar(4000) | YES | | | 异常信息 |
| DUEDATE_ | timestamp(3) | YES | | | 到期时间 |
| REPEAT_ | varchar(255) | YES | | | 重复配置 |
| HANDLER_TYPE_ | varchar(255) | YES | | | 处理器类型 |
| HANDLER_CFG_ | varchar(4000) | YES | | | 处理器配置 |
| TENANT_ID_ | varchar(255) | YES | | "" | 租户ID |

### act_ru_task
**业务含义**: Activiti运行时任务表，存储当前需要人工处理的用户任务

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| REV_ | int(11) | YES | | | 版本号 |
| EXECUTION_ID_ | varchar(64) | YES | MUL | | 执行实例ID，多重索引 |
| PROC_INST_ID_ | varchar(64) | YES | MUL | | 流程实例ID，多重索引 |
| PROC_DEF_ID_ | varchar(64) | YES | MUL | | 流程定义ID，多重索引 |
| NAME_ | varchar(255) | YES | | | 任务名称 |
| BUSINESS_KEY_ | varchar(255) | YES | | | 业务主键 |
| PARENT_TASK_ID_ | varchar(64) | YES | MUL | | 父任务ID，多重索引 |
| DESCRIPTION_ | varchar(4000) | YES | | | 任务描述 |
| TASK_DEF_KEY_ | varchar(255) | YES | | | 任务定义Key |
| OWNER_ | varchar(255) | YES | | | 任务拥有者 |
| ASSIGNEE_ | varchar(255) | YES | | | 任务执行人 |
| DELEGATION_ | varchar(64) | YES | | | 委托状态 |
| PRIORITY_ | int(11) | YES | | | 优先级 |
| CREATE_TIME_ | timestamp(3) | YES | MUL | | 创建时间，多重索引 |
| DUE_DATE_ | datetime(3) | YES | | | 到期时间 |
| CATEGORY_ | varchar(255) | YES | | | 任务分类 |
| SUSPENSION_STATE_ | int(11) | YES | | | 挂起状态 |
| TENANT_ID_ | varchar(255) | YES | | "" | 租户ID |
| FORM_KEY_ | varchar(255) | YES | | | 表单Key |
| CLAIM_TIME_ | datetime(3) | YES | | | 领取时间 |
| APP_VERSION_ | int(11) | YES | | | 应用版本 |

### act_ru_timer_job
**业务含义**: Activiti定时任务表，存储需要在特定时间执行的定时任务

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| REV_ | int(11) | YES | | | 版本号 |
| TYPE_ | varchar(255) | NO | | | 任务类型 |
| LOCK_EXP_TIME_ | timestamp(3) | YES | | | 锁过期时间 |
| LOCK_OWNER_ | varchar(255) | YES | | | 锁拥有者 |
| EXCLUSIVE_ | tinyint(1) | YES | | | 是否独占 |
| EXECUTION_ID_ | varchar(64) | YES | MUL | | 执行实例ID，多重索引 |
| PROCESS_INSTANCE_ID_ | varchar(64) | YES | MUL | | 流程实例ID，多重索引 |
| PROC_DEF_ID_ | varchar(64) | YES | MUL | | 流程定义ID，多重索引 |
| RETRIES_ | int(11) | YES | | | 重试次数 |
| EXCEPTION_STACK_ID_ | varchar(64) | YES | MUL | | 异常堆栈ID，多重索引 |
| EXCEPTION_MSG_ | varchar(4000) | YES | | | 异常信息 |
| DUEDATE_ | timestamp(3) | YES | | | 到期时间 |
| REPEAT_ | varchar(255) | YES | | | 重复配置 |
| HANDLER_TYPE_ | varchar(255) | YES | | | 处理器类型 |
| HANDLER_CFG_ | varchar(4000) | YES | | | 处理器配置 |
| TENANT_ID_ | varchar(255) | YES | | "" | 租户ID |

### act_ru_variable
**业务含义**: Activiti运行时变量表，存储当前流程和任务的变量数据

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| ID_ | varchar(64) | NO | PRI | | 主键ID |
| REV_ | int(11) | YES | | | 版本号 |
| TYPE_ | varchar(255) | NO | | | 变量类型 |
| NAME_ | varchar(255) | NO | | | 变量名称 |
| EXECUTION_ID_ | varchar(64) | YES | MUL | | 执行实例ID，多重索引 |
| PROC_INST_ID_ | varchar(64) | YES | MUL | | 流程实例ID，多重索引 |
| TASK_ID_ | varchar(64) | YES | MUL | | 任务ID，多重索引 |
| BYTEARRAY_ID_ | varchar(64) | YES | MUL | | 二进制数组ID，多重索引 |
| DOUBLE_ | double | YES | | | 双精度值 |
| LONG_ | bigint(20) | YES | | | 长整型值 |
| TEXT_ | varchar(4000) | YES | | | 文本值 |
| TEXT2_ | varchar(4000) | YES | | | 文本值2 |

## 业务扩展表详情

### workflow_process_agent_task_mapping
**业务含义**: 工作流代理任务映射表，用于记录任务代理关系，支持任务委托功能

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键ID，自增 |
| real_task_id | varchar(64) | NO | | "" | 真实任务ID |
| virtual_task_id | varchar(64) | NO | UNI | "" | 虚拟任务ID，唯一索引 |
| agent_assignee_id | bigint(20) | NO | | 0 | 代理执行人ID |
| origin_assignee_id | bigint(20) | NO | | 0 | 原始执行人ID |
| can_origin_receive_and_deal | tinyint(4) | NO | | 2 | 原执行人是否可接收处理 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |
| handle_status | int(11) | NO | | 0 | 处理状态 |

### workflow_process_aggregate_message
**业务含义**: 工作流聚合消息表，用于存储需要批量处理的聚合消息信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键ID，自增 |
| business | int(11) | NO | | 0 | 业务类型 |
| batch_id | bigint(20) | NO | UNI | 0 | 批次ID，唯一索引 |
| message_type | varchar(50) | NO | | "" | 消息类型 |
| content | varchar(2000) | NO | | "" | 消息内容 |
| create_time | bigint(20) | NO | | 0 | 创建时间，时间戳 |
| update_time | bigint(20) | NO | | 0 | 更新时间，时间戳 |

### workflow_process_assignee_change_modify_def
**业务含义**: 工作流执行人变更修改定义表，记录哪些流程定义支持执行人变更功能

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键ID，自增 |
| business | int(11) | NO | | 0 | 业务类型 |
| process_def_id | varchar(64) | NO | | "" | 流程定义ID |
| process_def_key | varchar(255) | NO | MUL | "" | 流程定义Key，多重索引 |
| create_time | bigint(20) | NO | | 0 | 创建时间，时间戳 |
| update_time | bigint(20) | NO | | 0 | 更新时间，时间戳 |

### workflow_process_node_advanced_setup
**业务含义**: 工作流节点高级设置表，存储流程节点的高级配置信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键ID，自增 |
| business | int(11) | NO | | 0 | 业务类型 |
| process_def_id | varchar(64) | NO | MUL | "" | 流程定义ID，多重索引 |
| node_id | varchar(255) | NO | | "" | 节点ID |
| value | json | YES | | | 配置值，JSON格式 |
| create_time | bigint(20) | NO | | 0 | 创建时间，时间戳 |
| update_time | bigint(20) | NO | | 0 | 更新时间，时间戳 |

### workflow_process_node_def
**业务含义**: 工作流节点定义表，存储流程中各个节点的基本定义信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键ID，自增 |
| business | int(11) | NO | | 0 | 业务类型 |
| process_def_id | varchar(64) | NO | MUL | "" | 流程定义ID，多重索引 |
| process_def_key | varchar(255) | NO | | "" | 流程定义Key |
| node_id | varchar(255) | NO | | "" | 节点ID |
| node_name | varchar(255) | NO | | "" | 节点名称 |
| node_type | int(11) | NO | | 0 | 节点类型 |
| order | int(11) | NO | | 0 | 节点顺序 |
| child_list | json | YES | | | 子节点列表，JSON格式 |
| extra | text | YES | | | 额外信息 |
| create_time | bigint(20) | NO | | 0 | 创建时间，时间戳 |
| update_time | bigint(20) | NO | | 0 | 更新时间，时间戳 |

### workflow_process_node_esign_setup
**业务含义**: 工作流节点电子签名设置表，存储需要电子签名的节点配置信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键ID，自增 |
| business | int(11) | NO | | 0 | 业务类型 |
| process_def_id | varchar(64) | NO | MUL | "" | 流程定义ID，多重索引 |
| node_id | varchar(255) | NO | | "" | 节点ID |
| value | json | YES | | | 电子签名配置，JSON格式 |
| create_time | bigint(20) | NO | | 0 | 创建时间，时间戳 |
| update_time | bigint(20) | NO | | 0 | 更新时间，时间戳 |

### workflow_process_node_extra_info
**业务含义**: 工作流节点扩展信息表，存储流程节点的额外扩展信息和配置

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键ID，自增 |
| business | int(11) | NO | | 0 | 业务类型 |
| process_def_id | varchar(64) | NO | MUL | "" | 流程定义ID，多重索引 |
| node_id | varchar(255) | NO | | "" | 节点ID |
| node_key | varchar(100) | NO | | | 节点Key |
| value | json | YES | | | 扩展信息值，JSON格式 |
| create_time | datetime | YES | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | YES | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

### workflow_process_node_setup
**业务含义**: 工作流节点基础设置表，存储流程节点的基本配置信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键ID，自增 |
| business | int(11) | NO | | 0 | 业务类型 |
| process_def_id | varchar(64) | NO | MUL | "" | 流程定义ID，多重索引 |
| node_id | varchar(255) | NO | | "" | 节点ID |
| value | json | YES | | | 设置值，JSON格式 |
| create_time | bigint(20) | NO | | 0 | 创建时间，时间戳 |
| update_time | bigint(20) | NO | | 0 | 更新时间，时间戳 |

## 数据库设计特点

### Activiti标准架构
- **完整的工作流引擎支持**：包含流程定义、实例管理、任务处理、历史记录等完整功能
- **多租户支持**：大部分表都支持TENANT_ID字段，实现多租户隔离
- **高性能设计**：通过合理的索引设计，支持高并发的流程执行

### 业务扩展设计
- **灵活的配置存储**：使用JSON字段存储复杂的业务配置
- **多业务类型支持**：通过business字段区分不同的业务场景
- **任务代理机制**：支持任务委托和代理执行功能
- **节点配置分离**：将不同类型的节点配置存储在不同的表中，便于管理

### 索引策略
- **查询优化**：基于process_def_id、proc_inst_id等关键字段建立索引
- **多字段组合索引**：支持复杂查询条件的快速检索
- **唯一性约束**：确保关键业务数据的唯一性

这个数据库设计充分体现了Activiti工作流引擎的标准架构，同时通过业务扩展表满足了特定的业务需求，如任务代理、节点配置、电子签名等功能。