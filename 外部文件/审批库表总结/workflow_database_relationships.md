# Workflow平台数据库表关联关系文档

## 概述

本文档描述了Moka HCM工作流系统三个核心数据库之间的表关联关系：
- **workflow_platform_core**: 工作流平台核心业务数据
- **workflow_form_platform**: 工作流表单平台数据  
- **workflow_process_platform**: 工作流流程引擎数据

## 核心关联字段

### 主要关联键
- **flow_def_id**: 工作流定义ID，连接三个数据库的核心字段
- **flow_inst_id**: 工作流实例ID，用于实例级别的关联
- **process_def_id**: 流程定义ID（Activiti标准）
- **process_inst_id**: 流程实例ID（Activiti标准）
- **form_def_id**: 表单定义ID
- **template_id**: 模板ID，连接模板配置
- **tenant_id**: 租户ID，多租户隔离
- **access**: 访问权限标识

## 数据库间关联关系

### 1. Core ←→ Form 关联关系

#### 1.1 工作流定义 ←→ 表单定义
```
workflow_core_flow_def.form_def_id 
    ↓
workflow_form_definition.id
```
- **业务含义**: 每个工作流定义关联一个表单定义
- **关系类型**: 一对一
- **用途**: 确定工作流使用的表单结构

#### 1.2 工作流实例 ←→ 表单数据
```
workflow_core_task_form_data_relation.form_data_id 
    ↓
workflow_form_data.id

workflow_core_task_form_data_relation.flow_inst_id
    ↓
workflow_core_flow_instance.flow_inst_id
```
- **业务含义**: 工作流任务与表单数据的关联
- **关系类型**: 多对多（通过中间表）
- **用途**: 存储每个任务节点的表单填写数据

#### 1.3 工作流草稿关联
```
workflow_core_draft_relation.draft_data_id
    ↓
workflow_form_draft_data.id

workflow_core_draft_relation.flow_def_id
    ↓
workflow_core_flow_def.flow_def_id
```
- **业务含义**: 工作流草稿数据关联
- **关系类型**: 一对一
- **用途**: 支持流程发起前的草稿保存功能

#### 1.4 表单权限关联
```
workflow_core_node_field_permission_relation.form_permission_id
    ↓
workflow_form_permission.id

workflow_core_node_field_permission_relation.flow_def_id
    ↓
workflow_core_flow_def.flow_def_id
```
- **业务含义**: 工作流节点的字段权限控制
- **关系类型**: 多对多
- **用途**: 控制不同节点上表单字段的可见性和编辑权限

### 2. Core ←→ Process 关联关系

#### 2.1 工作流定义 ←→ 流程定义
```
workflow_core_flow_def.process_def_key
    ↓
act_re_procdef.KEY_

workflow_core_flow_def.process_def_version
    ↓
act_re_procdef.VERSION_
```
- **业务含义**: 工作流定义与Activiti流程定义的映射
- **关系类型**: 一对一
- **用途**: 建立业务工作流与底层流程引擎的连接

#### 2.2 工作流实例 ←→ 流程实例
```
workflow_core_flow_instance.process_inst_id
    ↓
act_ru_execution.PROC_INST_ID_

workflow_core_flow_instance.process_inst_id
    ↓
act_hi_procinst.PROC_INST_ID_
```
- **业务含义**: 工作流实例与Activiti流程实例的映射
- **关系类型**: 一对一
- **用途**: 业务实例与流程引擎实例的关联

#### 2.3 流程节点配置关联
```
workflow_process_node_def.process_def_id
    ↓
act_re_procdef.ID_

workflow_core_flow_def.process_def_key
    ↓
workflow_process_node_def.process_def_key
```
- **业务含义**: 流程节点定义与配置的关联
- **关系类型**: 一对多
- **用途**: 为流程节点提供业务配置信息

#### 2.4 代理任务映射
```
workflow_process_agent_task_mapping.real_task_id
    ↓
act_ru_task.ID_

workflow_core_agent_config.agent_assignee_id/origin_assignee_id
    ↓
workflow_process_agent_task_mapping.agent_assignee_id/origin_assignee_id
```
- **业务含义**: 任务代理关系的映射
- **关系类型**: 一对一
- **用途**: 支持任务委托和代理功能

### 3. Form ←→ Process 间接关联

#### 3.1 通过Core数据库的间接关联
```
workflow_form_definition.id
    ↓
workflow_core_flow_def.form_def_id
    ↓
workflow_core_flow_def.process_def_key
    ↓
act_re_procdef.KEY_
```
- **业务含义**: 表单定义与流程定义的间接关联
- **关系类型**: 间接一对一
- **用途**: 确定特定流程使用的表单结构

#### 3.2 模板配置关联
```
workflow_template_conf_repository.template_id
    ↓
workflow_core_flow_def.template_id
    ↓
workflow_core_flow_def.process_def_key
    ↓
workflow_process_node_def.process_def_key
```
- **业务含义**: 模板配置、工作流定义、流程节点的关联
- **关系类型**: 间接多对多
- **用途**: 模板驱动的工作流配置

## 数据流转关系

### 1. 工作流定义阶段
```
模板配置(Form) → 工作流定义(Core) → 流程定义(Process)
    ↓                    ↓                 ↓
template_conf     flow_def_id        process_def_key
repository        form_def_id        node configurations
```

### 2. 工作流实例运行阶段
```
表单数据(Form) ← 工作流实例(Core) → 流程实例(Process)
    ↓                ↓                    ↓
form_data      flow_inst_id         process_inst_id
draft_data     task_form_relation   task_instances
```

### 3. 权限控制流转
```
表单权限(Form) ← 节点权限关联(Core) → 节点配置(Process)
    ↓                  ↓                    ↓
form_permission   node_field_permission   node_setup
field_repository  relation               node_advanced_setup
```

## 关键业务场景的表关联

### 场景1: 创建工作流定义
1. **workflow_template_conf_repository** → 获取模板配置
2. **workflow_form_definition** → 创建表单定义
3. **workflow_core_flow_def** → 创建工作流定义，关联表单和模板
4. **act_re_procdef** → 部署流程定义
5. **workflow_process_node_def** → 创建节点配置

### 场景2: 发起工作流实例
1. **workflow_core_flow_def** → 获取工作流定义
2. **workflow_form_definition** → 获取表单结构
3. **workflow_form_data** → 保存表单数据
4. **workflow_core_flow_instance** → 创建流程实例
5. **act_ru_execution** → 启动流程执行

### 场景3: 处理工作流任务
1. **act_ru_task** → 获取当前任务
2. **workflow_process_agent_task_mapping** → 检查代理关系
3. **workflow_form_permission** → 获取字段权限
4. **workflow_form_data** → 保存/更新表单数据
5. **workflow_core_task_form_data_relation** → 关联任务与表单数据

### 场景4: 查询工作流历史
1. **act_hi_procinst** → 获取历史流程实例
2. **workflow_core_flow_instance** → 获取业务实例信息
3. **act_hi_taskinst** → 获取历史任务信息
4. **workflow_core_task_form_data_relation** → 关联的表单数据
5. **workflow_form_data** → 获取具体表单数据

## 性能优化建议

### 1. 索引优化
- **flow_def_id**: 在所有相关表上建立索引
- **flow_inst_id**: 实例查询的关键索引
- **process_def_id/process_inst_id**: Activiti标准索引
- **tenant_id + access**: 多租户查询组合索引

### 2. 查询优化策略
- 使用**JOIN**查询减少数据库往返次数
- 针对高频查询场景建立**视图**
- 历史数据查询考虑**分表分库**策略
- 大数据量场景使用**分页查询**

### 3. 数据一致性
- 关键业务操作使用**事务**保证一致性
- 跨数据库操作考虑**分布式事务**
- 定期进行**数据一致性校验**
- 重要关联关系设置**外键约束**（开发环境）

## 监控和维护

### 1. 关联关系监控
- 监控**孤立数据**（无关联的记录）
- 检查**关联完整性**（确保外键关系正确）
- 统计**关联查询性能**

### 2. 数据清理策略
- 定期清理**历史数据**
- 删除**无效关联记录**
- 归档**长期不用的流程定义**

这个关联关系文档为开发人员提供了全面的数据库表关系视图，有助于理解业务逻辑、优化查询性能和维护数据一致性。