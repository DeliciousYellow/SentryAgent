# workflow_platform_core 数据库表结构文档

## 数据库概述
- 数据库名称：workflow_platform_core
- 数据库用途：工作流平台核心业务数据存储
- 表总数：39张

## 表结构详情

### log_test
**业务含义**: 日志测试表，用于系统日志测试

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | int(11) | NO | PRI | | 主键，自增 |
| time | varchar(100) | YES | | | 时间 |

#### 索引信息
- **PRIMARY**: 主键索引 (id)

### workflow_core_agent_config
**业务含义**: 工作流核心代理配置表，用于存储工作流代理人设置

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| tenant_id | varchar(180) | YES | | "" | 租户ID |
| bu_id | varchar(180) | YES | | "" | 业务单元ID |
| access | bigint(20) | NO | MUL | 0 | 访问权限，多重索引 |
| is_revoke | tinyint(4) | NO | | 1 | 是否撤销 |
| agent_assignee_id | bigint(20) | NO | | 0 | 代理人ID |
| origin_assignee_id | bigint(20) | NO | | 0 | 原受理人ID |
| can_original_receive_and_deal | tinyint(4) | NO | | 1 | 原人是否可接收处理 |
| start_time | date | NO | | | 开始时间 |
| end_time | date | NO | | | 结束时间 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |
| agent_assignee_name | varchar(50) | NO | | | 代理人姓名 |
| origin_assignee_name | varchar(50) | NO | | | 原受理人姓名 |
| agent_flow_list | json | NO | | | 代理工作流列表 |

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **idx_access**: 普通索引 (access)

### workflow_core_aggregate_message
**业务含义**: 工作流核心聚合消息表，用于存储聚合的工作流消息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| access | bigint(20) | NO | | 0 | 访问权限 |
| tenant_id | varchar(180) | NO | | "" | 租户ID |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| batch_id | bigint(20) | NO | MUL | 0 | 批次ID，多重索引 |
| message_type | varchar(50) | NO | | "" | 消息类型 |
| content | json | YES | | | 消息内容 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **uniq_idx_batch_id**: 唯一索引 (batch_id)

### workflow_core_aggregate_message_notify_task
**业务含义**: 工作流核心聚合消息通知任务表，用于管理消息通知任务

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| tenant_id | varchar(60) | NO | | "" | 租户ID |
| bu_id | varchar(60) | NO | | "" | 业务单元ID |
| access | bigint(20) | NO | | 0 | 访问权限 |
| employee_id | bigint(20) | NO | | 0 | 员工ID |
| task_instance_id | varchar(64) | NO | | "" | 任务实例ID |
| flow_instance_id | bigint(20) | NO | | 0 | 工作流实例ID |
| template_id | bigint(20) | NO | | 0 | 模板ID |
| template_name | varchar(255) | NO | | "" | 模板名称 |
| message_type | int(11) | NO | | 0 | 消息类型 |
| extra | text | YES | | | 扩展信息 |
| create_time | bigint(20) | NO | MUL | 0 | 创建时间，多重索引 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **idx_create_time**: 普通索引 (create_time)

### workflow_core_basic_data_operation_record
**业务含义**: 工作流核心基础数据操作记录表，用于记录基础数据的操作历史

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| tenant_id | varchar(60) | NO | | "" | 租户ID |
| bu_id | varchar(60) | NO | | "" | 业务单元ID |
| access | bigint(20) | NO | MUL | 0 | 访问权限，多重索引 |
| biz_data_type | int(11) | NO | | 0 | 业务数据类型 |
| biz_data_id | varchar(100) | NO | | "" | 业务数据ID |
| biz_uniq_key | varchar(32) | NO | | "" | 业务唯一键 |
| biz_data_name | text | YES | | | 业务数据名称 |
| operation_type | int(11) | NO | | 0 | 操作类型 |
| status | tinyint(4) | NO | | 0 | 状态 |
| operation_record_id | varchar(64) | NO | | "" | 操作记录ID |
| operation_value | text | YES | | | 操作值 |
| extra | text | YES | | | 扩展信息 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **idx_access**: 普通索引 (access)

### workflow_core_biz_field_operation_record
**业务含义**: 工作流核心业务字段操作记录表，用于记录业务字段的操作历史

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| tenant_id | varchar(60) | NO | | "" | 租户ID |
| bu_id | varchar(60) | NO | | "" | 业务单元ID |
| access | bigint(20) | NO | MUL | 0 | 访问权限，多重索引 |
| biz_uniq_key | varchar(32) | NO | | "" | 业务唯一键 |
| biz_field_name | text | YES | | | 业务字段名称 |
| operation_type | int(11) | NO | | 0 | 操作类型 |
| status | tinyint(4) | NO | | 0 | 状态 |
| operation_record_id | varchar(64) | NO | | "" | 操作记录ID |
| operation_value | text | YES | | | 操作值 |
| extra | text | YES | | | 扩展信息 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **idx_access**: 普通索引 (access)

### workflow_core_csm_config
**业务含义**: 工作流核心CSM配置表，用于存储客户成功管理相关配置

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| tenant_id | varchar(180) | YES | | "" | 租户ID |
| bu_id | varchar(180) | YES | | "" | 业务单元ID |
| product | bigint(20) | YES | MUL | 0 | 产品，多重索引 |
| config_key | varchar(50) | YES | | | 配置键 |
| config_key_desc | varchar(100) | YES | | | 配置键描述 |
| config_value | text | YES | | | 配置值 |
| create_time | datetime | YES | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | YES | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **idx_product**: 普通索引 (product)

### workflow_core_detail_log
**业务含义**: 工作流核心详细日志表，用于记录工作流执行的详细日志

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) unsigned | NO | PRI | | 主键，自增 |
| access | bigint(20) | NO | MUL | 0 | 访问权限，多重索引 |
| tenant_id | varchar(180) | NO | | "" | 租户ID |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| flow_inst_id | bigint(20) | NO | | 0 | 工作流实例ID |
| node_id | varchar(255) | NO | | "" | 节点ID |
| content | text | YES | | | 日志内容 |
| trace_id | varchar(255) | NO | | "" | 追踪ID |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **idx_access**: 普通索引 (access)

### workflow_core_draft_relation
**业务含义**: 工作流核心草稿关系表，用于建立工作流与草稿数据的关联关系

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) unsigned | NO | PRI | | 主键，自增 |
| access | bigint(20) | NO | | 0 | 访问权限 |
| tenant_id | varchar(180) | NO | | "" | 租户ID |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| current_user_id | bigint(20) unsigned | NO | MUL | 0 | 当前用户ID，多重索引 |
| flow_def_id | varchar(180) | NO | | "" | 工作流定义ID |
| draft_data_id | bigint(20) unsigned | NO | | 0 | 草稿数据ID |
| create_time | bigint(20) | NO | | | 创建时间 |
| update_time | bigint(20) | NO | | | 更新时间 |

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **idx_applicant_current_user_workflow**: 复合索引 (current_user_id, flow_def_id)

### workflow_core_execute_path_cache
**业务含义**: 工作流核心执行路径缓存表，用于缓存工作流执行路径信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) unsigned | NO | PRI | | 主键，自增 |
| access | bigint(20) | NO | MUL | 0 | 访问权限，多重索引 |
| tenant_id | varchar(180) | NO | | "" | 租户ID |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| flow_instance_id | bigint(20) | NO | | 0 | 工作流实例ID |
| content | text | YES | | | 缓存内容 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **idx_access**: 普通索引 (access)

### workflow_core_flow_backlog_search_field
**业务含义**: 工作流核心待办搜索字段表，用于配置工作流待办列表的搜索字段

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| access | int(11) | NO | MUL | 1 | 访问权限，多重索引 |
| tenant_id | varchar(180) | NO | | "" | 租户ID |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| field_key | varchar(255) | NO | | "" | 字段键 |
| field_name | varchar(255) | NO | | "" | 字段名称 |
| field_uniq_key | varchar(100) | NO | | "" | 字段唯一键 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **idx_access**: 普通索引 (access)

### workflow_core_flow_def
**业务含义**: 工作流核心工作流定义表，用于存储工作流定义的核心信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| tenant_id | varchar(180) | NO | MUL | "" | 租户ID，多重索引 |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| access | bigint(20) | NO | MUL | 0 | 访问权限，多重索引 |
| flow_def_key | bigint(20) | NO | MUL | 0 | 工作流定义键，多重索引 |
| flow_def_version | bigint(20) | NO | | 0 | 工作流定义版本 |
| is_latest_visible_version | tinyint(4) | NO | | 0 | 是否最新可见版本 |
| flow_def_id | varchar(180) | NO | UNI | "" | 工作流定义ID，唯一索引 |
| flow_name | varchar(255) | NO | | "" | 工作流名称 |
| start_type | int(1) | NO | | 0 | 启动类型 |
| form_def_id | bigint(20) | NO | | 0 | 表单定义ID |
| template_id | bigint(20) | NO | MUL | 0 | 模板ID，多重索引 |
| template_version | int(11) | NO | | 0 | 模板版本 |
| process_def_key | varchar(255) | NO | | 0 | 流程定义键 |
| process_def_version | int(11) | NO | | 0 | 流程定义版本 |
| remark | varchar(1000) | NO | | "" | 备注 |
| operator_id | bigint(20) unsigned | NO | | 0 | 操作员ID |
| allow_revoke_on_the_way | tinyint(4) | NO | | 0 | 是否允许中途撤销 |
| choose_applicant_by_self | tinyint(4) | NO | | 0 | 是否可自选申请人 |
| flow_def_status | int(11) | NO | | 0 | 工作流定义状态 |
| flow_op_conf | text | YES | | | 工作流操作配置 |
| form_def_version | int(20) | NO | | 1 | 表单定义版本 |
| release_time | bigint(20) | NO | | 0 | 发布时间 |
| modify_time | bigint(20) | NO | | 0 | 修改时间 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **uniq_idx_flow_def_id**: 唯一索引 (flow_def_id)
- **idx_tenant_id**: 普通索引 (tenant_id)
- **idx_access**: 普通索引 (access)
- **idx_flow_def_key**: 普通索引 (flow_def_key)
- **idx_template_id**: 普通索引 (template_id)

### workflow_core_flow_def_admin_relation
**业务含义**: 工作流核心工作流定义管理员关系表，用于建立工作流定义与管理员的关联关系

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| access | bigint(20) | NO | | 0 | 访问权限 |
| tenant_id | varchar(180) | NO | MUL | "" | 租户ID，多重索引 |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| admin_id | bigint(20) | NO | | 0 | 管理员ID |
| flow_def_id | varchar(180) | NO | | "" | 工作流定义ID |
| type | int(11) | NO | | 0 | 类型 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

### workflow_core_flow_def_admin_role_relation
**业务含义**: 工作流核心工作流定义管理员角色关系表，用于建立工作流定义与管理员角色的关联关系

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| access | bigint(20) | NO | | 0 | 访问权限 |
| tenant_id | varchar(180) | NO | MUL | "" | 租户ID，多重索引 |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| role_id | bigint(20) | NO | | 0 | 角色ID |
| flow_def_id | varchar(180) | NO | | "" | 工作流定义ID |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

### workflow_core_flow_def_basic_data_ref_record
**业务含义**: 工作流核心工作流定义基础数据引用记录表，用于记录工作流定义引用基础数据的关系

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| tenant_id | varchar(60) | NO | | "" | 租户ID |
| bu_id | varchar(60) | NO | | "" | 业务单元ID |
| access | bigint(20) | NO | MUL | 0 | 访问权限，多重索引 |
| operation_record_id | varchar(64) | NO | | "" | 操作记录ID |
| index_id | varchar(64) | NO | | "" | 索引ID |
| biz_uniq_key | varchar(32) | NO | | "" | 业务唯一键 |
| flow_def_id | varchar(60) | NO | | "" | 工作流定义ID |
| template_id | bigint(20) | NO | | 0 | 模板ID |
| ref_record_id | varchar(64) | NO | | "" | 引用记录ID |
| ref_record_status | int(11) | NO | | 0 | 引用记录状态 |
| operator_id | int(11) | NO | | 0 | 操作员ID |
| status | tinyint(4) | NO | | 0 | 状态 |
| extra | text | YES | | | 扩展信息 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

### workflow_core_flow_def_chain
**业务含义**: 工作流定义链表，用于建立新旧系统工作流定义的映射关系

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | int(10) unsigned | NO | PRI | | 主键，自增 |
| flow_def_key | bigint(20) | NO | UNI | | 工作流定义键，唯一索引 |
| flow_def_id | varchar(180) | NO | MUL | "" | 工作流定义ID，多重索引 |
| old_sys_flow_def_id | bigint(20) | NO | MUL | | 旧系统工作流定义ID，多重索引 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |
| status | tinyint(4) | NO | | 0 | 状态 |

### workflow_core_flow_def_group
**业务含义**: 工作流定义分组表，用于对工作流定义进行分组管理

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| group_id | bigint(20) | NO | UNI | | 分组ID，唯一索引 |
| tenant_id | varchar(255) | NO | MUL | 0 | 租户ID，多重索引 |
| bu_id | varchar(255) | NO | | 0 | 业务单元ID |
| access | bigint(20) | NO | | 0 | 访问权限 |
| name | varchar(255) | NO | | "" | 分组名称 |
| stop | tinyint(4) | NO | | 0 | 是否停用 |
| is_deleted | tinyint(4) | NO | | 0 | 是否删除 |
| hire_mode | int(11) | NO | | 0 | 招聘模式 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

### workflow_core_flow_def_group_relation
**业务含义**: 工作流定义与分组关系表，建立工作流定义与分组的多对多关系

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| access | bigint(20) | NO | | 0 | 访问权限 |
| tenant_id | varchar(180) | NO | MUL | "" | 租户ID，多重索引 |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| group_id | bigint(20) | NO | | 0 | 分组ID |
| flow_def_id | varchar(180) | NO | | "" | 工作流定义ID |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

### workflow_core_flow_def_index_basic_data
**业务含义**: 工作流定义索引基础数据表，用于存储工作流定义相关的业务数据索引信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| tenant_id | varchar(60) | NO | | "" | 租户ID |
| bu_id | varchar(60) | NO | | "" | 业务单元ID |
| access | bigint(20) | NO | MUL | 0 | 访问权限，多重索引 |
| index_id | varchar(64) | NO | | "" | 索引ID |
| biz_data_type | int(11) | NO | | 0 | 业务数据类型 |
| biz_data_id | varchar(100) | NO | | "" | 业务数据ID |
| biz_uniq_key | varchar(32) | NO | | "" | 业务唯一键 |
| flow_def_id | varchar(60) | NO | | "" | 工作流定义ID |
| status | tinyint(4) | NO | | 0 | 状态 |
| extra | text | YES | | | 扩展信息 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

### workflow_core_flow_def_index_field
**业务含义**: 工作流定义索引字段表，用于存储工作流定义相关的字段索引信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| tenant_id | varchar(60) | NO | | "" | 租户ID |
| bu_id | varchar(60) | NO | | "" | 业务单元ID |
| access | bigint(20) | NO | MUL | 0 | 访问权限，多重索引 |
| biz_uniq_key | varchar(32) | NO | | "" | 业务唯一键 |
| uniq_key | varchar(100) | NO | | "" | 唯一键 |
| field_type | int(11) | NO | | 0 | 字段类型 |
| flow_def_id | varchar(60) | NO | | "" | 工作流定义ID |
| status | tinyint(4) | NO | | 0 | 状态 |
| extra | text | YES | | | 扩展信息 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

### workflow_core_flow_def_index_specific_person
**业务含义**: 工作流定义索引特定人员表，用于存储工作流定义相关的特定人员索引信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| tenant_id | varchar(60) | NO | | "" | 租户ID |
| bu_id | varchar(60) | NO | | "" | 业务单元ID |
| access | bigint(20) | NO | MUL | 0 | 访问权限，多重索引 |
| employee_id | bigint(20) | NO | MUL | 0 | 员工ID，多重索引 |
| flow_def_id | varchar(60) | NO | MUL | "" | 工作流定义ID，多重索引 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

### workflow_core_flow_def_initiator_relation
**业务含义**: 工作流定义发起人关系表，用于存储工作流定义的发起人设置详情

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| access | bigint(20) | NO | | 0 | 访问权限 |
| tenant_id | varchar(180) | NO | | "" | 租户ID |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| flow_def_id | varchar(180) | NO | MUL | "" | 工作流定义ID，多重索引 |
| detail | text | YES | | | 发起人配置详情 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

### workflow_core_flow_def_temp
**业务含义**: 工作流定义临时表，用于存储工作流定义的临时数据或草稿

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) unsigned | NO | PRI | | 主键，自增 |
| tenant_id | varchar(180) | NO | MUL | "" | 租户ID，多重索引 |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| access | bigint(20) | NO | | 0 | 访问权限 |
| flow_def_key | bigint(20) | NO | | 0 | 工作流定义键 |
| flow_def_version | bigint(20) | NO | | 0 | 工作流定义版本 |
| flow_def_id | varchar(180) | NO | UNI | "" | 工作流定义ID，唯一索引 |
| flow_name | varchar(255) | NO | | "" | 工作流名称 |
| start_type | int(1) | NO | | 0 | 启动类型 |
| form_def_id | bigint(20) | NO | | 0 | 表单定义ID |
| template_id | bigint(20) | NO | MUL | 0 | 模板ID，多重索引 |
| template_version | int(11) | NO | | 0 | 模板版本 |
| process_def_key | varchar(255) | NO | | 0 | 流程定义键 |
| process_def_version | int(11) | NO | | 0 | 流程定义版本 |
| remark | varchar(1000) | NO | | "" | 备注 |
| operator_id | bigint(20) unsigned | NO | | 0 | 操作员ID |
| allow_revoke_on_the_way | tinyint(4) | NO | | 0 | 是否允许中途撤销 |
| choose_applicant_by_self | tinyint(4) | NO | | 0 | 是否可自选申请人 |
| flow_def_status | int(11) | NO | | 0 | 工作流定义状态 |
| flow_op_conf | text | YES | | | 工作流操作配置 |
| form_def_version | int(20) | NO | | 1 | 表单定义版本 |
| release_time | bigint(20) | NO | | 0 | 发布时间 |
| modify_time | bigint(20) | NO | | 0 | 修改时间 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |
| root_flow_def_key | bigint(20) | YES | | 0 | 根工作流定义键 |

### workflow_core_flow_def_upgrade_task
**业务含义**: 工作流定义升级任务表，用于记录工作流定义的升级任务状态

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| tenant_id | varchar(60) | NO | | "" | 租户ID |
| bu_id | varchar(60) | NO | | "" | 业务单元ID |
| access | bigint(20) | NO | MUL | 0 | 访问权限，多重索引 |
| operation_record_id | varchar(64) | NO | | "" | 操作记录ID |
| biz_uniq_key | varchar(32) | NO | | "" | 业务唯一键 |
| flow_def_id | varchar(60) | NO | | "" | 工作流定义ID |
| template_id | bigint(20) | NO | | 0 | 模板ID |
| task_id | bigint(20) | NO | | 0 | 任务ID |
| task_status | int(11) | NO | | 0 | 任务状态 |
| status | tinyint(4) | NO | | 0 | 状态 |
| fail_reason | text | YES | | | 失败原因 |
| task_operator | bigint(20) | NO | | 0 | 任务操作员 |
| extra | text | YES | | | 扩展信息 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

### workflow_core_flow_instance
**业务含义**: 工作流实例表，用于存储工作流实例的核心信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| access | bigint(20) | NO | MUL | 0 | 访问权限，多重索引 |
| tenant_id | varchar(180) | NO | MUL | "" | 租户ID，多重索引 |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| applicant_id | bigint(20) | NO | | 0 | 申请人ID |
| initiator_id | bigint(20) | NO | | 0 | 发起人ID |
| flow_inst_id | bigint(20) | NO | UNI | 0 | 流程实例ID，唯一索引 |
| flow_def_id | varchar(255) | NO | MUL | "" | 工作流定义ID，多重索引 |
| process_inst_id | varchar(255) | NO | MUL | "" | 流程实例ID，多重索引 |
| revoke_flow_inst_id | bigint(20) | NO | MUL | 0 | 撤销流程实例ID，多重索引 |
| process_inst_status | int(11) | NO | | | 流程实例状态 |
| initiate_time | bigint(20) | NO | | | 发起时间 |
| modify_time | bigint(20) | NO | MUL | | 修改时间，多重索引 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |
| applicant_entity_id | varchar(100) | NO | | "" | 申请实体ID |
| source | int(11) | YES | | 0 | 来源 |
| status | int(11) | NO | | 1 | 状态 |
| instance_form_def_id | bigint(20) | NO | | 0 | 实例表单定义ID |
| instance_form_def_version | bigint(20) | NO | | 1 | 实例表单定义版本 |
| associated_flow_inst_id | bigint(20) | NO | MUL | 0 | 关联流程实例ID，多重索引 |
| modify_flow_inst_count | int(11) | YES | | 0 | 修改流程实例计数 |
| flow_type | int(11) | NO | | 0 | 流程类型 |
| starter_type | int(11) | NO | | 0 | 发起人类型 |

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **idx_flow_inst_id**: 唯一索引 (flow_inst_id)
- **idx_access**: 普通索引 (access)
- **idx_tenant_id**: 普通索引 (tenant_id)
- **idx_flow_def_id**: 普通索引 (flow_def_id)
- **idx_process_inst_id**: 普通索引 (process_inst_id)
- **idx_revoke_flow_inst_id**: 普通索引 (revoke_flow_inst_id)
- **idx_modify_time**: 普通索引 (modify_time)
- **idx_associated_flow_inst_id**: 普通索引 (associated_flow_inst_id)

### workflow_core_flow_instance_batch_relation
**业务含义**: 工作流实例批次关系表，用于建立工作流实例与批次的关联关系

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| access | bigint(20) | NO | | 0 | 访问权限 |
| tenant_id | varchar(180) | NO | | "" | 租户ID |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| flow_inst_id | bigint(20) | NO | MUL | 0 | 工作流实例ID，多重索引 |
| batch_no | bigint(20) | NO | MUL | 0 | 批次号，多重索引 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

### workflow_core_flow_instance_batch_relation_test
**业务含义**: 工作流实例批次关系测试表，用于测试环境的工作流实例与批次关联关系

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) unsigned | NO | PRI | | 主键，自增 |
| access | bigint(20) | NO | | 0 | 访问权限 |
| tenant_id | varchar(180) | NO | | "" | 租户ID |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| flow_inst_id | bigint(20) | NO | MUL | 0 | 工作流实例ID，多重索引 |
| batch_no | bigint(20) | NO | MUL | 0 | 批次号，多重索引 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

### workflow_core_flow_instance_dt_chat_relation
**业务含义**: 工作流实例钉钉聊天关系表，用于建立工作流实例与钉钉聊天的关联关系

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) unsigned | NO | PRI | | 主键，自增 |
| tenant_id | varchar(50) | NO | | 0 | 租户ID |
| bu_id | varchar(50) | NO | | 0 | 业务单元ID |
| access | bigint(20) | NO | MUL | 0 | 访问权限，多重索引 |
| user_id | bigint(20) | NO | | 0 | 用户ID |
| flow_inst_id | bigint(20) | NO | | 0 | 工作流实例ID |
| business_id | varchar(128) | NO | | "" | 业务ID |
| dt_chat_link | varchar(256) | NO | | "" | 钉钉聊天链接 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |
| status | int(11) | NO | | 1 | 状态 |

### workflow_core_flow_instance_operation_source_relation
**业务含义**: 工作流实例操作来源关系表，用于记录工作流实例的操作来源信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| tenant_id | varchar(180) | YES | | "" | 租户ID |
| bu_id | varchar(180) | YES | | "" | 业务单元ID |
| access | bigint(20) | YES | MUL | 0 | 访问权限，多重索引 |
| flow_inst_id | bigint(20) | YES | | 0 | 工作流实例ID |
| relation_value | text | YES | | | 关系值 |
| create_time | datetime | YES | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | YES | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

### workflow_core_message_aggregate_notify_config
**业务含义**: 工作流消息聚合通知配置表，用于存储消息聚合通知的配置信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| tenant_id | varchar(60) | NO | | "" | 租户ID |
| bu_id | varchar(60) | NO | | "" | 业务单元ID |
| access | bigint(20) | NO | MUL | 0 | 访问权限，多重索引 |
| unique_id | varchar(32) | NO | | "" | 唯一标识 |
| status | int(11) | NO | | 0 | 状态 |
| content | text | YES | | | 配置内容 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

### workflow_core_node_field_permission_relation
**业务含义**: 工作流节点字段权限关系表，用于建立工作流节点与字段权限的关联关系

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) unsigned | NO | PRI | | 主键，自增 |
| access | bigint(20) | NO | | 0 | 访问权限 |
| tenant_id | varchar(180) | NO | | "" | 租户ID |
| bu_id | varchar(180) | NO | | 0 | 业务单元ID |
| flow_def_id | varchar(180) | NO | MUL | "" | 工作流定义ID，多重索引 |
| node_id | varchar(64) | NO | MUL | "" | 节点ID，多重索引 |
| node_type | int(11) | NO | | 0 | 节点类型 |
| form_permission_id | bigint(20) unsigned | NO | | 0 | 表单权限ID |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

### workflow_core_print_template_conf
**业务含义**: 工作流打印模板配置表，用于存储工作流的打印模板配置信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| tenant_id | varchar(180) | YES | | "" | 租户ID |
| bu_id | varchar(180) | YES | | "" | 业务单元ID |
| access | bigint(20) | YES | MUL | 0 | 访问权限，多重索引 |
| flow_def_id | varchar(180) | YES | | "" | 工作流定义ID |
| conf | text | YES | | | 配置内容 |
| create_time | datetime | YES | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | YES | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

### workflow_core_push_flow_def_record
**业务含义**: 工作流定义推送记录表，用于记录工作流定义推送到业务系统的记录

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| tenant_id | varchar(180) | NO | | "" | 租户ID |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| access | bigint(20) | NO | MUL | 0 | 访问权限，多重索引 |
| platform_flow_def_id | varchar(180) | NO | | "" | 平台工作流定义ID |
| biz_flow_def_id | varchar(180) | NO | | "" | 业务工作流定义ID |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

### workflow_core_push_flow_instance_record
**业务含义**: 工作流实例推送记录表，用于记录工作流实例推送到业务系统的记录

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| tenant_id | varchar(180) | NO | | "" | 租户ID |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| access | bigint(20) | NO | MUL | 0 | 访问权限，多重索引 |
| platform_flow_instance_id | bigint(20) | NO | | 0 | 平台工作流实例ID |
| biz_flow_instance_id | varchar(180) | NO | | "" | 业务工作流实例ID |
| biz_flow_def_id | varchar(180) | NO | | "" | 业务工作流定义ID |
| platform_flow_def_id | varchar(180) | NO | | "" | 平台工作流定义ID |
| data | json | YES | | | JSON数据 |
| data_sync_id | bigint(20) | NO | | 0 | 数据同步ID |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |
| data_sync_status | int(11) | NO | | 0 | 数据同步状态 |
| status | int(1) | NO | | 0 | 状态 |

### workflow_core_sync_node_id_mapping
**业务含义**: 工作流节点ID同步映射表，用于建立平台节点ID与业务节点ID的映射关系

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| tenant_id | varchar(180) | NO | | "" | 租户ID |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| access | bigint(20) | NO | MUL | 0 | 访问权限，多重索引 |
| platform_flow_def_id | varchar(180) | NO | | "" | 平台工作流定义ID |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |
| platform_node_id | varchar(255) | NO | | "" | 平台节点ID |
| biz_node_id | varchar(50) | NO | | "" | 业务节点ID |

### workflow_core_sync_task_id_mapping
**业务含义**: 工作流任务ID同步映射表，用于建立平台任务实例ID与业务任务实例ID的映射关系

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| tenant_id | varchar(180) | NO | | "" | 租户ID |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| access | bigint(20) | NO | MUL | 0 | 访问权限，多重索引 |
| platform_flow_instance_id | bigint(20) | NO | | 0 | 平台工作流实例ID |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |
| platform_task_instance_id | varchar(255) | NO | | "" | 平台任务实例ID |
| biz_task_instance_id | varchar(100) | NO | | "" | 业务任务实例ID |
| assignee | bigint(20) | NO | | 0 | 任务分配人 |
| platform_node_id | varchar(255) | NO | | "" | 平台节点ID |
| biz_node_id | varchar(50) | NO | | 接入方节点定义id | 业务节点ID |

### workflow_core_task_form_data_relation
**业务含义**: 工作流任务表单数据关系表，用于建立工作流任务与表单数据的关联关系

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| access | bigint(20) | NO | MUL | 0 | 访问权限，多重索引 |
| tenant_id | varchar(180) | NO | | "" | 租户ID |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| flow_inst_id | bigint(20) | NO | MUL | 0 | 工作流实例ID，多重索引 |
| form_data_id | bigint(20) | NO | | 0 | 表单数据ID |
| node_type | int(11) | NO | | 0 | 节点类型 |
| task_inst_id | varchar(100) | NO | MUL | "" | 任务实例ID，多重索引 |
| commit_time | bigint(20) | NO | | | 提交时间 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

### workflow_core_third_interface_key
**业务含义**: 工作流第三方接口键表，用于存储第三方系统接口的配置信息

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | int(11) | YES | | | 主键 |
| interface_key | varchar(255) | YES | | | 接口键 |
| access | varchar(20) | YES | | | 访问权限 |
| application_name | varchar(255) | YES | | | 应用名称 |
| feign_url | varchar(255) | YES | | | Feign接口URL |
| module_name | varchar(255) | YES | | | 模块名称 |
| time_out | bigint(20) | YES | | | 超时时间 |
| status | int(11) | YES | | | 状态 |
| description | varchar(50) | YES | | | 描述 |

### workflow_health_check_result_record
**业务含义**: 工作流健康检查结果记录表，用于存储工作流系统的健康检查结果

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | bigint(20) | NO | PRI | | 主键，自增 |
| access | bigint(20) | NO | MUL | 0 | 访问权限，多重索引 |
| tenant_id | varchar(180) | NO | | "" | 租户ID |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| data_id | varchar(255) | NO | MUL | "" | 数据ID，多重索引 |
| data_type | tinyint(4) | NO | | 0 | 数据类型 |
| bad_case_type | varchar(255) | NO | | "" | 异常类型 |
| extra | text | NO | | | 额外信息 |
| handle_status | tinyint(4) | NO | | 0 | 处理状态 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |

### workflow_message_urge_rule
**业务含义**: 工作流消息催办规则表，用于存储工作流任务催办的规则配置

| 字段名 | 类型 | 是否允许NULL | 键类型 | 默认值 | 备注 |
|--------|------|-------------|---------|--------|------|
| id | int(11) | NO | PRI | | 主键，自增 |
| tenant_id | varchar(180) | NO | | "" | 租户ID |
| bu_id | varchar(180) | NO | | "" | 业务单元ID |
| rule_status | tinyint(4) | NO | | 0 | 规则状态 |
| urge_frequency | tinyint(4) | NO | | 0 | 催办频率 |
| trigger_time | varchar(10) | NO | | 10:00 | 触发时间 |
| weekdays | varchar(100) | NO | | [] | 工作日配置 |
| before_days | int(10) | NO | | 0 | 提前天数 |
| flow_def_id | varchar(180) | NO | | "" | 工作流定义ID |
| flow_def_rule_type | int(11) | NO | | 0 | 工作流定义规则类型 |
| creater | bigint(20) | NO | | 0 | 创建人 |
| updater | bigint(20) | NO | | 0 | 更新人 |
| create_time | datetime | NO | | CURRENT_TIMESTAMP | 创建时间 |
| update_time | datetime | NO | | CURRENT_TIMESTAMP | 更新时间，自动更新 |
| access | bigint(20) | NO | | 1 | 访问权限 |
