# workflow_form_platform 数据库文档

## 数据库概述

workflow_form_platform 数据库是 Moka HCM 工作流系统的表单平台核心数据库，负责管理工作流表单的定义、数据、权限和模板配置等功能。该数据库支持多租户架构，为不同的企业和业务单元提供独立的表单管理服务。

## 表结构详情

### 1. custom_field_assign_data_way
**业务含义**：自定义字段数据分配方式配置表

| 字段名 | 类型 | 是否NULL | 键类型 | 默认值 | 扩展信息 | 说明 |
|--------|------|----------|---------|---------|----------|------|
| id | bigint(20) | NO | PRI | null | auto_increment | 主键ID |
| field_type | int(11) | NO |  | 0 |  | 字段类型 |
| assign_way_type | int(11) | NO |  | 0 |  | 分配方式类型 |
| assign_way | json | NO |  | null |  | 分配方式配置信息 |
| create_time | bigint(20) | NO |  | 0 |  | 创建时间 |
| update_time | bigint(20) | NO |  | 0 |  | 更新时间 |

**主键**：id

#### 索引信息
- **PRIMARY**: 主键索引 (id)

---

### 2. hcm_abs_overtime_userule_rest_config
**业务含义**：HCM考勤加班用户规则休息配置表

| 字段名 | 类型 | 是否NULL | 键类型 | 默认值 | 扩展信息 | 说明 |
|--------|------|----------|---------|---------|----------|------|
| id | bigint(20) unsigned | NO | PRI | null | auto_increment | 主键ID |
| ent_id | bigint(20) | NO | MUL | 0 |  | 企业ID |
| bu_id | bigint(20) | NO |  | 0 |  | 业务单元ID |
| name | varchar(200) | NO |  | "" |  | 配置名称 |
| rule_type_id | bigint(20) | NO |  | 0 |  | 规则类型ID |
| rest_type | varchar(30) | NO |  | "" |  | 休息类型 |
| config | text | YES |  | null |  | 配置信息 |
| create_time | datetime | NO |  | CURRENT_TIMESTAMP |  | 创建时间 |
| update_time | datetime | NO |  | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP | 更新时间 |
| creator | bigint(20) | NO |  | 0 |  | 创建人ID |
| updater | bigint(20) | NO |  | 0 |  | 更新人ID |

**主键**：id

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **idx_ent_bu_rule_type_id**: 复合索引 (ent_id, bu_id, rule_type_id)

---

### 3. system_field_repository
**业务含义**：系统字段仓库表，存储系统预定义的字段配置

| 字段名 | 类型 | 是否NULL | 键类型 | 默认值 | 扩展信息 | 说明 |
|--------|------|----------|---------|---------|----------|------|
| id | bigint(20) | NO | PRI | null | auto_increment | 主键ID |
| product | bigint(11) | NO | MUL | 1 |  | 产品线ID |
| business | int(11) | NO |  | 0 |  | 业务类型 |
| field_id | bigint(20) | NO | UNI | 0 |  | 字段ID |
| field_key | varchar(100) | NO |  | "" |  | 字段标识 |
| field_name | varchar(255) | NO |  | "" |  | 字段名称 |
| field_type | int(11) | NO |  | 0 |  | 字段类型 |
| source | json | NO |  | null |  | 数据源配置 |
| assign_ways | json | NO |  | null |  | 赋值方式 |
| required | int(11) | NO |  | 0 |  | 是否必填 |
| can_edit_required | int(1) | YES |  | 0 |  | 是否可编辑必填属性 |
| can_edit_value | int(1) | YES |  | 0 |  | 是否可编辑值 |
| branch_condition | int(1) | NO |  | 0 |  | 分支条件 |
| usable | int(11) | NO |  | 1 |  | 是否可用 |
| uniq_key | varchar(100) | NO | UNI | "" |  | 唯一标识 |
| create_time | bigint(20) | NO |  | 0 |  | 创建时间 |
| update_time | bigint(20) | NO |  | 0 |  | 更新时间 |
| properties | json | NO |  | null |  | 字段属性 |

**主键**：id

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **uniq_idx_field_id**: 唯一索引 (field_id)
- **uniq_idx_uniq_key**: 唯一索引 (uniq_key)
- **idx_product_usable**: 复合索引 (product, usable)

---

### 4. system_field_repository_bak
**业务含义**：系统字段仓库备份表

| 字段名 | 类型 | 是否NULL | 键类型 | 默认值 | 扩展信息 | 说明 |
|--------|------|----------|---------|---------|----------|------|
| id | bigint(20) | NO | PRI | null | auto_increment | 主键ID |
| product | bigint(11) | NO |  | 1 |  | 产品线ID |
| business | int(11) | NO |  | 0 |  | 业务类型 |
| field_id | bigint(20) | NO | UNI | 0 |  | 字段ID |
| field_key | varchar(100) | NO |  | "" |  | 字段标识 |
| field_name | varchar(255) | NO |  | "" |  | 字段名称 |
| field_type | int(11) | NO |  | 0 |  | 字段类型 |
| source | json | NO |  | null |  | 数据源配置 |
| assign_ways | json | NO |  | null |  | 赋值方式 |
| required | int(11) | NO |  | 0 |  | 是否必填 |
| can_edit_required | int(1) | YES |  | 0 |  | 是否可编辑必填属性 |
| can_edit_value | int(1) | YES |  | 0 |  | 是否可编辑值 |
| usable | int(11) | NO |  | 1 |  | 是否可用 |
| uniq_key | varchar(100) | NO | UNI | "" |  | 唯一标识 |
| create_time | bigint(20) | NO |  | 0 |  | 创建时间 |
| update_time | bigint(20) | NO |  | 0 |  | 更新时间 |
| properties | json | NO |  | null |  | 字段属性 |

**主键**：id

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **uniq_idx_field_id**: 唯一索引 (field_id)
- **uniq_idx_uniq_key**: 唯一索引 (uniq_key)

---

### 5. tenant_field_repository
**业务含义**：租户字段仓库表，存储租户自定义的字段配置

| 字段名 | 类型 | 是否NULL | 键类型 | 默认值 | 扩展信息 | 说明 |
|--------|------|----------|---------|---------|----------|------|
| id | bigint(20) | NO | PRI | null | auto_increment | 主键ID |
| access | bigint(11) | NO | MUL | 1 |  | 访问标识 |
| tenant_id | varchar(180) | NO | MUL | "" |  | 租户ID |
| bu_id | varchar(180) | NO |  | "" |  | 业务单元ID |
| field_id | bigint(20) | NO | UNI | 0 |  | 字段ID |
| field_key | varchar(100) | NO | MUL | "" |  | 字段标识 |
| field_name | varchar(255) | NO |  | "" |  | 字段名称 |
| field_type | int(11) | NO |  | 0 |  | 字段类型 |
| properties | json | NO |  | null |  | 字段属性 |
| source | json | NO |  | null |  | 数据源配置 |
| assign_ways | json | NO |  | null |  | 赋值方式 |
| required | tinyint(1) | NO |  | 0 |  | 是否必填 |
| can_edit_required | tinyint(1) | YES |  | 0 |  | 是否可编辑必填属性 |
| can_edit_value | tinyint(1) | YES |  | 0 |  | 是否可编辑值 |
| branch_condition | tinyint(1) | NO |  | 0 |  | 分支条件 |
| usable | tinyint(1) | NO |  | 1 |  | 是否可用 |
| uniq_key | varchar(100) | NO | UNI | null |  | 唯一标识 |
| create_time | bigint(20) | NO |  | 0 |  | 创建时间 |
| update_time | bigint(20) | NO |  | 0 |  | 更新时间 |

**主键**：id

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **uniq_idx_field_id**: 唯一索引 (field_id)
- **uniq_idx_uniq_key**: 唯一索引 (uniq_key)
- **idx_access_tenant_bu**: 复合索引 (access, tenant_id, bu_id)
- **idx_field_key**: 普通索引 (field_key)
- **idx_tenant_id_bu_id_access_usable**: 复合索引 (tenant_id, bu_id, access, usable)

---

### 6. tenant_field_repository_bak
**业务含义**：租户字段仓库备份表

| 字段名 | 类型 | 是否NULL | 键类型 | 默认值 | 扩展信息 | 说明 |
|--------|------|----------|---------|---------|----------|------|
| id | bigint(20) | NO | PRI | null | auto_increment | 主键ID |
| product | bigint(11) | NO |  | 1 |  | 产品线ID |
| business | int(11) | NO |  | 1 |  | 业务类型 |
| tenant_id | bigint(20) | NO |  | 0 |  | 租户ID |
| bu_id | bigint(20) | NO |  | 0 |  | 业务单元ID |
| field_id | bigint(20) | NO | UNI | 0 |  | 字段ID |
| field_key | varchar(100) | NO |  | "" |  | 字段标识 |
| field_name | varchar(255) | NO |  | "" |  | 字段名称 |
| field_type | int(11) | NO |  | 0 |  | 字段类型 |
| source | json | NO |  | null |  | 数据源配置 |
| assign_ways | json | NO |  | null |  | 赋值方式 |
| required | int(11) | NO |  | 0 |  | 是否必填 |
| can_edit_required | int(1) | YES |  | 0 |  | 是否可编辑必填属性 |
| can_edit_value | int(1) | YES |  | 0 |  | 是否可编辑值 |
| usable | int(11) | NO |  | 1 |  | 是否可用 |
| uniq_key | varchar(100) | NO | UNI | null |  | 唯一标识 |
| create_time | bigint(20) | NO |  | 0 |  | 创建时间 |
| update_time | bigint(20) | NO |  | 0 |  | 更新时间 |

**主键**：id

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **uniq_idx_field_id**: 唯一索引 (field_id)
- **uniq_idx_uniq_key**: 唯一索引 (uniq_key)

---

### 7. workflow_form_data
**业务含义**：工作流表单数据表，存储表单的实际数据内容

| 字段名 | 类型 | 是否NULL | 键类型 | 默认值 | 扩展信息 | 说明 |
|--------|------|----------|---------|---------|----------|------|
| id | bigint(20) unsigned | NO | PRI | null | auto_increment | 主键ID |
| access | bigint(20) | NO |  | 1 |  | 访问标识 |
| tenant_id | varchar(180) | NO | MUL | "" |  | 租户ID |
| bu_id | varchar(180) | NO |  | "" |  | 业务单元ID |
| form_data_id | bigint(20) unsigned | NO | MUL | 0 |  | 表单数据ID |
| version | int(10) unsigned | NO |  | 0 |  | 版本号 |
| form_def_id | bigint(20) unsigned | NO | MUL | 0 |  | 表单定义ID |
| form_def_version | int(10) unsigned | NO |  | 0 |  | 表单定义版本 |
| value | json | NO |  | null |  | 表单数据值 |
| encrypt_value | longtext | YES |  | null |  | 加密值 |
| type | int(1) unsigned | NO |  | 0 |  | 数据类型 |
| encry_type | int(1) unsigned | NO |  | 0 |  | 加密类型 |
| last_version_id | bigint(20) | NO |  | 1 |  | 最后版本ID |
| is_deleted | tinyint(3) unsigned | NO |  | 0 |  | 是否删除 |
| create_time | datetime | NO |  | CURRENT_TIMESTAMP |  | 创建时间 |
| update_time | datetime | NO |  | CURRENT_TIMESTAMP |  | 更新时间 |

**主键**：id

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **idx_form_id_version**: 复合索引 (form_data_id, version)
- **idx_id_version_tenant_bu**: 复合索引 (form_def_id, form_def_version, tenant_id, bu_id)
- **idx_tenant_id**: 复合索引 (tenant_id, id)

---

### 8. workflow_form_definition
**业务含义**：工作流表单定义表，存储表单的结构和配置

| 字段名 | 类型 | 是否NULL | 键类型 | 默认值 | 扩展信息 | 说明 |
|--------|------|----------|---------|---------|----------|------|
| id | bigint(20) unsigned | NO | PRI | null | auto_increment | 主键ID |
| form_def_id | bigint(20) | NO | MUL | 0 |  | 表单定义ID |
| version | int(10) unsigned | NO |  | 0 |  | 版本号 |
| product | bigint(20) | NO | MUL | 1 |  | 产品线ID |
| tenant_id | varchar(180) | NO | MUL | "" |  | 租户ID |
| bu_id | varchar(180) | NO |  | "" |  | 业务单元ID |
| template_id | bigint(20) | NO |  | 0 |  | 模板ID |
| template_version | int(11) | NO |  | 0 |  | 模板版本 |
| form_field_conf | json | NO |  | null |  | 表单字段配置 |
| link_rule_conf | json | YES |  | null |  | 联动规则配置 |
| linkage_list | json | YES |  | null |  | 联动列表 |
| hide_preset_linkage_ids | varchar(100) | YES |  | null |  | 隐藏预设联动ID |
| create_time | datetime | NO |  | CURRENT_TIMESTAMP |  | 创建时间 |
| update_time | datetime | NO |  | CURRENT_TIMESTAMP |  | 更新时间 |
| form_def_scope | int(11) | NO |  | 0 |  | 表单定义范围 |
| employees_by_department | tinyint(1) | YES |  | null |  | 按部门显示员工 |

**主键**：id

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **idx_id_version**: 复合索引 (form_def_id, version)
- **idx_product_tenant_id**: 复合索引 (product, tenant_id, id)
- **idx_tenant**: 普通索引 (tenant_id)
- **def_version_ent_bu**: 复合索引 (tenant_id, bu_id)

---

### 9. workflow_form_definition_bak
**业务含义**：工作流表单定义备份表

| 字段名 | 类型 | 是否NULL | 键类型 | 默认值 | 扩展信息 | 说明 |
|--------|------|----------|---------|---------|----------|------|
| id | bigint(20) unsigned | NO | PRI | null | auto_increment | 主键ID |
| workflow_def_id | bigint(20) | NO | MUL | 0 |  | 工作流定义ID |
| form_def_id | bigint(20) | NO |  | 0 |  | 表单定义ID |
| version | int(10) unsigned | NO |  | 0 |  | 版本号 |
| product | bigint(20) | NO |  | 1 |  | 产品线ID |
| business | bigint(20) | NO |  | 0 |  | 业务类型 |
| tenant_id | bigint(20) | NO |  | 0 |  | 租户ID |
| bu_id | bigint(20) | NO |  | 0 |  | 业务单元ID |
| template_id | bigint(20) | NO |  | 0 |  | 模板ID |
| template_version | int(11) | NO |  | 0 |  | 模板版本 |
| form_field_conf | json | NO |  | null |  | 表单字段配置 |
| link_rule_conf | json | YES |  | null |  | 联动规则配置 |
| create_time | datetime | NO |  | CURRENT_TIMESTAMP |  | 创建时间 |
| update_time | datetime | NO |  | CURRENT_TIMESTAMP |  | 更新时间 |

**主键**：id

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **def_version_ent_bu**: 复合索引 (workflow_def_id, tenant_id, bu_id)

---

### 10. workflow_form_draft_data
**业务含义**：工作流表单草稿数据表，存储用户编辑中的表单草稿

| 字段名 | 类型 | 是否NULL | 键类型 | 默认值 | 扩展信息 | 说明 |
|--------|------|----------|---------|---------|----------|------|
| id | bigint(20) unsigned | NO | PRI | null | auto_increment | 主键ID |
| product | bigint(20) | NO |  | 1 |  | 产品线ID |
| business | bigint(20) | NO |  | 0 |  | 业务类型 |
| tenant_id | varchar(180) | NO |  | "" |  | 租户ID |
| bu_id | varchar(180) | NO |  | "" |  | 业务单元ID |
| draft_data_id | bigint(20) unsigned | NO | MUL | 0 |  | 草稿数据ID |
| current_user_id | bigint(20) unsigned | NO |  | 0 |  | 当前用户ID |
| form_def_id | bigint(20) unsigned | NO | MUL | 0 |  | 表单定义ID |
| form_def_version | int(10) unsigned | NO |  | 0 |  | 表单定义版本 |
| value | json | NO |  | null |  | 草稿数据值 |
| extend | json | NO |  | null |  | 扩展信息 |
| client_type | tinyint(3) unsigned | NO |  | 0 |  | 客户端类型 |
| is_deleted | tinyint(3) unsigned | NO |  | 0 |  | 是否删除 |
| create_time | datetime | NO |  | CURRENT_TIMESTAMP |  | 创建时间 |
| update_time | datetime | NO |  | CURRENT_TIMESTAMP |  | 更新时间 |

**主键**：id

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **idx_draft_user_is_deleted**: 复合索引 (draft_data_id, current_user_id, is_deleted)
- **idx_form_def_id_version_user_is_deleted**: 复合索引 (form_def_id, form_def_version, current_user_id, is_deleted)

---

### 11. workflow_form_landing_portion
**业务含义**：工作流表单数据落地部分配置表，管理表单数据的落地逻辑

| 字段名 | 类型 | 是否NULL | 键类型 | 默认值 | 扩展信息 | 说明 |
|--------|------|----------|---------|---------|----------|------|
| id | bigint(20) unsigned | NO | PRI | null | auto_increment | 主键ID |
| portion_id | bigint(20) | NO |  | null |  | 部分ID |
| group_id | bigint(20) | NO |  | null |  | 分组ID |
| landing_id | bigint(20) | NO |  | null |  | 落地ID |
| pre_portion_id | bigint(20) | NO |  | 0 |  | 前一部分ID |
| next_portion_id | bigint(20) | NO |  | 0 |  | 后一部分ID |
| portion_type | int(11) | NO |  | null |  | 部分类型 |
| current_status | varchar(100) | NO |  | null |  | 当前状态 |
| landing_action_info_list | text | NO |  | null |  | 落地动作信息列表 |
| access | bigint(20) | NO | MUL | null |  | 访问标识 |
| tenant_id | varchar(50) | NO |  | null |  | 租户ID |
| bu_id | varchar(50) | NO |  | null |  | 业务单元ID |
| flow_inst_id | bigint(20) | NO |  | null |  | 流程实例ID |
| task_inst_id | varchar(100) | YES |  | null |  | 任务实例ID |
| flow_status | int(11) | NO |  | null |  | 流程状态 |
| template_id | int(11) | NO |  | null |  | 模板ID |
| landing_interface | varchar(255) | NO |  | null |  | 落地接口 |
| rollback_interface | varchar(255) | YES |  | null |  | 回滚接口 |
| need_callback | tinyint(1) | NO |  | 0 |  | 是否需要回调 |
| data_landing_req | mediumtext | YES |  | null |  | 数据落地请求 |
| create_time | datetime | NO |  | CURRENT_TIMESTAMP |  | 创建时间 |
| update_time | datetime | NO | MUL | CURRENT_TIMESTAMP |  | 更新时间 |

**主键**：id

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **idx_workflow_form_landing_portion_access_inst**: 复合索引 (access, tenant_id, bu_id, flow_inst_id)
- **idx_workflow_form_landing_portion_access_portion**: 复合索引 (access, tenant_id, bu_id, portion_id)
- **idx_workflow_form_landing_portion_update_time**: 普通索引 (update_time)

---

### 12. workflow_form_permission
**业务含义**：工作流表单权限表，管理表单字段的访问权限

| 字段名 | 类型 | 是否NULL | 键类型 | 默认值 | 扩展信息 | 说明 |
|--------|------|----------|---------|---------|----------|------|
| id | bigint(20) unsigned | NO | PRI | null | auto_increment | 主键ID |
| access | bigint(11) | NO | MUL | 1 |  | 访问标识 |
| tenant_id | varchar(180) | NO |  | "" |  | 租户ID |
| bu_id | varchar(180) | NO |  | "" |  | 业务单元ID |
| form_permission_id | bigint(20) unsigned | NO |  | 0 |  | 表单权限ID |
| form_def_id | bigint(20) unsigned | NO | MUL | 0 |  | 表单定义ID |
| form_def_version | int(10) unsigned | NO |  | 0 |  | 表单定义版本 |
| value | json | YES |  | null |  | 权限值 |
| field_property_permission | json | YES |  | null |  | 字段属性权限 |
| field_permission_mode | int(11) | NO |  | 0 |  | 字段权限模式 |
| is_deleted | tinyint(3) unsigned | NO |  | 0 |  | 是否删除 |
| create_time | datetime | NO |  | CURRENT_TIMESTAMP |  | 创建时间 |
| update_time | datetime | NO |  | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP | 更新时间 |

**主键**：id

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **idx_form_def_id_form_def_version_detail_id**: 复合索引 (form_def_id, form_def_version, form_permission_id)
- **index_name**: 复合索引 (access, tenant_id, bu_id, form_permission_id)

---

### 13. workflow_form_snapshot
**业务含义**：工作流表单快照表，存储表单在特定时间点的状态

| 字段名 | 类型 | 是否NULL | 键类型 | 默认值 | 扩展信息 | 说明 |
|--------|------|----------|---------|---------|----------|------|
| id | bigint(20) unsigned | NO | PRI | null | auto_increment | 主键ID |
| access | bigint(20) | NO |  | 0 |  | 访问标识 |
| tenant_id | varchar(180) | NO |  | "" |  | 租户ID |
| bu_id | varchar(180) | NO |  | "" |  | 业务单元ID |
| applicant_id | bigint(20) | NO |  | 0 |  | 申请人ID |
| applicant_entity_id | varchar(100) | NO |  | "" |  | 申请人实体ID |
| initiator_id | bigint(20) | NO |  | 0 |  | 发起人ID |
| flow_inst_id | bigint(20) | NO | UNI | 0 |  | 流程实例ID |
| value | json | NO |  | null |  | 快照数据值 |
| create_time | datetime | NO |  | CURRENT_TIMESTAMP |  | 创建时间 |
| update_time | datetime | NO |  | CURRENT_TIMESTAMP |  | 更新时间 |

**主键**：id

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **uk_flow_inst_id**: 唯一索引 (flow_inst_id)

---

### 14. workflow_preview_form_data
**业务含义**：工作流预览表单数据表，存储表单预览时的数据

| 字段名 | 类型 | 是否NULL | 键类型 | 默认值 | 扩展信息 | 说明 |
|--------|------|----------|---------|---------|----------|------|
| id | bigint(20) unsigned | NO | PRI | null | auto_increment | 主键ID |
| product | bigint(20) | NO |  | 1 |  | 产品线ID |
| business | bigint(20) | NO |  | 0 |  | 业务类型 |
| tenant_id | varchar(180) | NO |  | "" |  | 租户ID |
| bu_id | varchar(180) | NO |  | "" |  | 业务单元ID |
| preview_form_data_id | bigint(20) unsigned | NO | MUL | 0 |  | 预览表单数据ID |
| form_def_id | bigint(20) unsigned | NO |  | 0 |  | 表单定义ID |
| form_def_version | int(10) unsigned | NO |  | 0 |  | 表单定义版本 |
| value | json | NO |  | null |  | 预览数据值 |
| last_version_id | bigint(20) | NO |  | 0 |  | 最后版本ID |
| is_deleted | tinyint(3) unsigned | NO |  | 0 |  | 是否删除 |
| create_time | datetime | NO |  | null |  | 创建时间 |
| update_time | datetime | NO |  | null |  | 更新时间 |

**主键**：id

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **idx_preview_form_data_id**: 普通索引 (preview_form_data_id)

---

### 15. workflow_template_conf_repository
**业务含义**：工作流模板配置仓库表，存储工作流模板的完整配置

| 字段名 | 类型 | 是否NULL | 键类型 | 默认值 | 扩展信息 | 说明 |
|--------|------|----------|---------|---------|----------|------|
| id | bigint(20) | NO | PRI | null | auto_increment | 主键ID |
| template_id | bigint(20) | NO | MUL | 0 |  | 模板ID |
| product | bigint(11) | NO |  | 1 |  | 产品线ID |
| business | int(11) | NO |  | 0 |  | 业务类型 |
| hire_mode | int(11) | YES |  | 0 |  | 招聘模式 |
| logo_url | varchar(255) | NO |  | "" |  | Logo URL |
| logo_id | int(11) | NO |  | 0 |  | Logo ID |
| launch_type | varchar(20) | NO |  | ["1"] |  | 启动类型 |
| choose_by_self | int(1) | YES |  | 1 |  | 是否可自选 |
| description | varchar(500) | NO |  | "" |  | 描述 |
| name | varchar(255) | NO |  | "" |  | 模板名称 |
| gray_rule | text | NO |  | null |  | 灰度规则 |
| form_conf | json | NO |  | null |  | 表单配置 |
| version | int(11) | NO |  | 0 |  | 版本号 |
| deleted | int(11) | NO |  | 0 |  | 是否删除 |
| create_time | bigint(20) | NO |  | 0 |  | 创建时间 |
| landing_conf | json | NO |  | null |  | 落地配置 |
| update_time | bigint(20) | NO |  | 0 |  | 更新时间 |
| need_drafts | tinyint(1) | NO |  | 1 |  | 是否支持草稿 |
| need_encrypt | int(11) | YES |  | 2 |  | 是否需要加密 |
| environment_type | int(1) | YES |  | 0 |  | 环境类型 |
| base_conf | json | YES |  | null |  | 基础配置 |
| allow_batch_approve | tinyint(1) | NO |  | 1 |  | 允许批量审批 |
| form_def_config_mode | int(1) | YES |  | 0 |  | 表单定义配置模式 |
| config_require_in_node | int(1) | NO |  | 0 |  | 节点中配置必填 |
| operator | varchar(255) | YES |  | "" |  | 操作人 |
| operator_id | bigint(20) | NO |  | 0 |  | 操作人ID |
| support_e_sign | int(11) | NO |  | 0 |  | 支持电子签名 |
| employees_by_department | int(11) | NO |  | 0 |  | 按部门显示员工 |
| need_inform | tinyint(1) | NO |  | 0 |  | 是否需要通知 |
| upgrade_content | json | YES |  | null |  | 升级内容 |
| support_msg_rule | int(1) | NO |  | 0 |  | 支持消息规则 |

**主键**：id

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **uniq_idx_template_id**: 唯一复合索引 (template_id, version)

---

### 16. workflow_template_conf_repository_bak
**业务含义**：工作流模板配置仓库备份表

| 字段名 | 类型 | 是否NULL | 键类型 | 默认值 | 扩展信息 | 说明 |
|--------|------|----------|---------|---------|----------|------|
| id | bigint(20) | NO | PRI | null | auto_increment | 主键ID |
| template_id | bigint(20) | NO | MUL | 0 |  | 模板ID |
| product | bigint(11) | NO |  | 1 |  | 产品线ID |
| business | int(11) | NO |  | 0 |  | 业务类型 |
| logo_url | varchar(255) | NO |  | "" |  | Logo URL |
| logo_id | int(11) | NO |  | 0 |  | Logo ID |
| launch_type | varchar(20) | NO |  | ["1"] |  | 启动类型 |
| choose_by_self | int(1) | YES |  | 1 |  | 是否可自选 |
| desc | varchar(500) | NO |  | "" |  | 描述 |
| name | varchar(255) | NO |  | "" |  | 模板名称 |
| gray_rule | varchar(1000) | NO |  | [*] |  | 灰度规则 |
| form_conf | json | NO |  | null |  | 表单配置 |
| version | int(11) | NO |  | 0 |  | 版本号 |
| deleted | int(11) | NO |  | 0 |  | 是否删除 |
| create_time | bigint(20) | NO |  | 0 |  | 创建时间 |
| landing_conf | json | NO |  | null |  | 落地配置 |
| update_time | bigint(20) | NO |  | 0 |  | 更新时间 |

**主键**：id

#### 索引信息
- **PRIMARY**: 主键索引 (id)
- **uniq_idx_template_id**: 唯一复合索引 (template_id, version)

---

### 17. workflow_template_conf_repository_gray
**业务含义**：工作流模板配置仓库灰度表，用于灰度发布的模板配置

| 字段名 | 类型 | 是否NULL | 键类型 | 默认值 | 扩展信息 | 说明 |
|--------|------|----------|---------|---------|----------|------|
| id | bigint(20) | NO | PRI | null | auto_increment | 主键ID |
| template_id | bigint(20) | NO | MUL | 0 |  | 模板ID |
| product | bigint(11) | NO |  | 1 |  | 产品线ID |
| business | int(11) | NO |  | 0 |  | 业务类型 |
| hire_mode | int(11) | YES |  | 0 |  | 招聘模式 |
| logo_url | varchar(255) | NO |  | "" |  | Logo URL |
| logo_id | int(11) | NO |  | 0 |  | Logo ID |
| launch_type | varchar(20) | NO |  | ["1"] |  | 启动类型 |
| choose_by_self | int(1) | YES |  | 1 |  | 是否可自选 |
| description | varchar(500) | NO |  | "" |  | 描述 |
| name | varchar(255) | NO |  | "" |  | 模板名称 |
| gray_rule | text | NO |  | null |  | 灰度规则 |
| form_conf | json | NO |  | null |  | 表单配置 |
| version | int(11) | NO |  | 0 |  | 版本号 |
| deleted | int(11) | NO |  | 0 |  | 是否删除 |
| create_time | bigint(20) | NO |  | 0 |  | 创建时间 |
| landing_conf | json | NO |  | null |  | 落地配置 |
| update_time | bigint(20) | NO |  | 0 |  | 更新时间 |
| need_drafts | tinyint(1) | NO |  | 1 |  | 是否支持草稿 |
| need_encrypt | int(11) | YES |  | 2 |  | 是否需要加密 |
| environment_type | int(1) | YES |  | 0 |  | 环境类型 |
| base_conf | json | YES |  | null |  | 基础配置 |
| allow_batch_approve | tinyint(1) | NO |  | 1 |  | 允许批量审批 |
| form_def_config_mode | int(1) | YES |  | 0 |  | 表单定义配置模式 |
| config_require_in_node | int(1) | NO |  | 0 |  | 节点中配置必填 |
| operator | varchar(255) | YES |  | "" |  | 操作人 |
| operator_id | bigint(20) | NO |  | 0 |  | 操作人ID |
| support_e_sign | int(11) | NO |  | 0 |  | 支持电子签名 |
| employees_by_department | int(11) | NO |  | 0 |  | 按部门显示员工 |
| need_inform | tinyint(1) | NO |  | 0 |  | 是否需要通知 |
| upgrade_content | json | YES |  | null |  | 升级内容 |
| support_msg_rule | int(1) | NO |  | 0 |  | 支持消息规则 |

**主键**：id  
**索引**：template_id (MUL)

---

### 18. workflow_template_operate_record
**业务含义**：工作流模板操作记录表，记录模板的操作历史

| 字段名 | 类型 | 是否NULL | 键类型 | 默认值 | 扩展信息 | 说明 |
|--------|------|----------|---------|---------|----------|------|
| id | bigint(20) | NO | PRI | null | auto_increment | 主键ID |
| operator_id | bigint(20) | YES |  | null |  | 操作人ID |
| operator_name | varchar(30) | YES |  | null |  | 操作人姓名 |
| module | int(11) | YES |  | null |  | 模块 |
| template_id | bigint(20) | YES |  | null |  | 模板ID |
| change_data | json | YES |  | null |  | 变更数据 |
| create_time | datetime | NO |  | CURRENT_TIMESTAMP |  | 创建时间 |
| operate_type | int(11) | YES |  | null |  | 操作类型 |

**主键**：id

---

### 19. workflow_template_preset_linkage
**业务含义**：工作流模板预设联动表，配置模板中的字段联动关系

| 字段名 | 类型 | 是否NULL | 键类型 | 默认值 | 扩展信息 | 说明 |
|--------|------|----------|---------|---------|----------|------|
| id | bigint(20) | NO | PRI | null | auto_increment | 主键ID |
| template_id | int(11) | NO |  | 0 |  | 模板ID |
| condition_list | json | NO |  | null |  | 条件列表 |
| behavior_list | json | NO |  | null |  | 行为列表 |

**主键**：id

---

## 数据库设计特点

### 多租户架构支持
- 大多数表都包含 `tenant_id` 和 `bu_id` 字段，支持多租户和多业务单元架构
- 通过 `access` 字段进行访问控制

### 版本管理
- 表单定义、模板配置等关键表都支持版本管理
- 提供备份表（带 `_bak` 后缀）用于数据备份和回滚

### JSON 存储
- 大量使用 JSON 字段存储复杂配置和数据，提供了灵活的数据结构支持
- 主要用于表单配置、权限配置、联动规则等复杂业务逻辑

### 数据安全
- 支持数据加密存储（`encrypt_value` 字段）
- 软删除机制（`is_deleted` 字段）
- 操作审计（操作记录表）

### 业务特性
- 支持草稿功能（`workflow_form_draft_data` 表）
- 支持表单预览（`workflow_preview_form_data` 表）
- 支持数据快照（`workflow_form_snapshot` 表）
- 灰度发布支持（`_gray` 后缀表）

---

*文档生成时间：2025-09-24*