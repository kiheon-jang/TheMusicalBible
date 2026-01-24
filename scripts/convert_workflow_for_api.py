#!/usr/bin/env python3
"""
n8n 워크플로우 JSON을 API 형식으로 변환
"""

import json
import sys

def convert_workflow(input_file, output_file):
    """워크플로우 JSON을 n8n API 형식으로 변환"""
    with open(input_file, 'r', encoding='utf-8') as f:
        workflow = json.load(f)
    
    # API 형식에 맞게 변환 (tags는 read-only이므로 제거)
    api_workflow = {
        "name": workflow.get("name", ""),
        "nodes": workflow.get("nodes", []),
        "connections": workflow.get("connections", {}),
        "settings": workflow.get("settings", {}),
        "staticData": workflow.get("staticData", None)
    }
    
    # credentials 제거 (나중에 수동 설정)
    for node in api_workflow["nodes"]:
        if "credentials" in node:
            # credentials 객체는 유지하되, ID만 제거
            node["credentials"] = {}
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(api_workflow, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 변환 완료: {input_file} -> {output_file}")

if __name__ == "__main__":
    workflows = [
        "workflows/init_database.json",
        "workflows/morning_batch.json",
        "workflows/evening_generation.json",
        "workflows/daily_monitoring.json"
    ]
    
    for workflow_file in workflows:
        output_file = workflow_file.replace('.json', '_api.json')
        try:
            convert_workflow(workflow_file, output_file)
        except Exception as e:
            print(f"❌ 오류: {workflow_file} - {e}")
