#!/usr/bin/env python3
"""
Analytics Dashboard
Comprehensive analytics and insights for the AI Writing Companion
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import numpy as np

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import framework and components
from framework.framework_tool import get_framework
from system_dashboard import SystemDashboard
from project_manager import ProjectManager


@dataclass
class AnalyticsData:
    """Analytics data structure"""
    timestamp: str
    user_id: str
    action_type: str
    action_details: Dict
    success: bool
    response_time: float
    system_component: str


class AnalyticsDashboard:
    """Comprehensive analytics dashboard"""
    
    def __init__(self, data_directory: str = "data/analytics"):
        self.data_directory = Path(data_directory)
        self.data_directory.mkdir(parents=True, exist_ok=True)
        
        self.framework = get_framework()
        self.system_dashboard = SystemDashboard()
        self.project_manager = ProjectManager()
        
        self.analytics_file = self.data_directory / "analytics.json"
        self.analytics_data = self.load_analytics()
    
    def load_analytics(self) -> List[AnalyticsData]:
        """Load analytics data from file"""
        if self.analytics_file.exists():
            try:
                with open(self.analytics_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    analytics = []
                    for item in data:
                        analytics.append(AnalyticsData(**item))
                    return analytics
            except Exception as e:
                print(f"Error loading analytics: {e}")
                return []
        return []
    
    def save_analytics(self):
        """Save analytics data to file"""
        try:
            data = [asdict(item) for item in self.analytics_data]
            with open(self.analytics_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving analytics: {e}")
    
    def record_action(self, user_id: str, action_type: str, action_details: Dict,
                     success: bool, response_time: float, system_component: str):
        """Record an analytics action"""
        analytics_item = AnalyticsData(
            timestamp=datetime.now().isoformat(),
            user_id=user_id,
            action_type=action_type,
            action_details=action_details,
            success=success,
            response_time=response_time,
            system_component=system_component
        )
        
        self.analytics_data.append(analytics_item)
        self.save_analytics()
    
    def get_user_analytics(self, user_id: str, time_period: str = "all") -> Dict:
        """Get analytics for a specific user"""
        user_data = [item for item in self.analytics_data if item.user_id == user_id]
        
        if time_period != "all":
            cutoff_date = self._get_cutoff_date(time_period)
            user_data = [item for item in user_data 
                        if datetime.fromisoformat(item.timestamp) >= cutoff_date]
        
        return self._analyze_user_data(user_data)
    
    def get_system_analytics(self, time_period: str = "all") -> Dict:
        """Get overall system analytics"""
        system_data = self.analytics_data.copy()
        
        if time_period != "all":
            cutoff_date = self._get_cutoff_date(time_period)
            system_data = [item for item in system_data 
                          if datetime.fromisoformat(item.timestamp) >= cutoff_date]
        
        return self._analyze_system_data(system_data)
    
    def get_component_analytics(self, component: str, time_period: str = "all") -> Dict:
        """Get analytics for a specific system component"""
        component_data = [item for item in self.analytics_data 
                         if item.system_component == component]
        
        if time_period != "all":
            cutoff_date = self._get_cutoff_date(time_period)
            component_data = [item for item in component_data 
                            if datetime.fromisoformat(item.timestamp) >= cutoff_date]
        
        return self._analyze_component_data(component_data)
    
    def _get_cutoff_date(self, time_period: str) -> datetime:
        """Get cutoff date for time period"""
        now = datetime.now()
        
        if time_period == "day":
            return now - timedelta(days=1)
        elif time_period == "week":
            return now - timedelta(weeks=1)
        elif time_period == "month":
            return now - timedelta(days=30)
        elif time_period == "quarter":
            return now - timedelta(days=90)
        elif time_period == "year":
            return now - timedelta(days=365)
        else:
            return datetime.min
    
    def _analyze_user_data(self, user_data: List[AnalyticsData]) -> Dict:
        """Analyze user-specific data"""
        if not user_data:
            return {}
        
        # Action type analysis
        action_types = Counter([item.action_type for item in user_data])
        
        # Success rate analysis
        success_count = sum(1 for item in user_data if item.success)
        success_rate = (success_count / len(user_data)) * 100
        
        # Response time analysis
        response_times = [item.response_time for item in user_data]
        avg_response_time = sum(response_times) / len(response_times)
        max_response_time = max(response_times)
        min_response_time = min(response_times)
        
        # Component usage analysis
        component_usage = Counter([item.system_component for item in user_data])
        
        # Time-based analysis
        hourly_usage = defaultdict(int)
        daily_usage = defaultdict(int)
        
        for item in user_data:
            timestamp = datetime.fromisoformat(item.timestamp)
            hour = timestamp.hour
            day = timestamp.strftime("%Y-%m-%d")
            hourly_usage[hour] += 1
            daily_usage[day] += 1
        
        return {
            "total_actions": len(user_data),
            "action_types": dict(action_types),
            "success_rate": round(success_rate, 2),
            "response_times": {
                "average": round(avg_response_time, 2),
                "maximum": round(max_response_time, 2),
                "minimum": round(min_response_time, 2)
            },
            "component_usage": dict(component_usage),
            "hourly_usage": dict(hourly_usage),
            "daily_usage": dict(daily_usage),
            "most_used_action": action_types.most_common(1)[0][0] if action_types else None,
            "most_used_component": component_usage.most_common(1)[0][0] if component_usage else None
        }
    
    def _analyze_system_data(self, system_data: List[AnalyticsData]) -> Dict:
        """Analyze overall system data"""
        if not system_data:
            return {}
        
        # Overall statistics
        total_actions = len(system_data)
        success_count = sum(1 for item in system_data if item.success)
        success_rate = (success_count / total_actions) * 100
        
        # Response time analysis
        response_times = [item.response_time for item in system_data]
        avg_response_time = sum(response_times) / len(response_times)
        
        # Component analysis
        component_usage = Counter([item.system_component for item in system_data])
        action_types = Counter([item.action_type for item in system_data])
        
        # User analysis
        user_activity = Counter([item.user_id for item in system_data])
        
        # Time-based analysis
        hourly_usage = defaultdict(int)
        daily_usage = defaultdict(int)
        
        for item in system_data:
            timestamp = datetime.fromisoformat(item.timestamp)
            hour = timestamp.hour
            day = timestamp.strftime("%Y-%m-%d")
            hourly_usage[hour] += 1
            daily_usage[day] += 1
        
        return {
            "total_actions": total_actions,
            "success_rate": round(success_rate, 2),
            "average_response_time": round(avg_response_time, 2),
            "component_usage": dict(component_usage),
            "action_types": dict(action_types),
            "user_activity": dict(user_activity),
            "hourly_usage": dict(hourly_usage),
            "daily_usage": dict(daily_usage),
            "most_active_user": user_activity.most_common(1)[0][0] if user_activity else None,
            "most_used_component": component_usage.most_common(1)[0][0] if component_usage else None,
            "most_common_action": action_types.most_common(1)[0][0] if action_types else None
        }
    
    def _analyze_component_data(self, component_data: List[AnalyticsData]) -> Dict:
        """Analyze component-specific data"""
        if not component_data:
            return {}
        
        # Component statistics
        total_actions = len(component_data)
        success_count = sum(1 for item in component_data if item.success)
        success_rate = (success_count / total_actions) * 100
        
        # Response time analysis
        response_times = [item.response_time for item in component_data]
        avg_response_time = sum(response_times) / len(response_times)
        
        # Action type analysis
        action_types = Counter([item.action_type for item in component_data])
        
        # User analysis
        user_activity = Counter([item.user_id for item in component_data])
        
        return {
            "total_actions": total_actions,
            "success_rate": round(success_rate, 2),
            "average_response_time": round(avg_response_time, 2),
            "action_types": dict(action_types),
            "user_activity": dict(user_activity),
            "most_common_action": action_types.most_common(1)[0][0] if action_types else None,
            "most_active_user": user_activity.most_common(1)[0][0] if user_activity else None
        }
    
    def generate_usage_report(self, time_period: str = "month") -> str:
        """Generate a comprehensive usage report"""
        system_analytics = self.get_system_analytics(time_period)
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           ANALYTICS DASHBOARD REPORT                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 SYSTEM USAGE REPORT ({time_period.upper()})
────────────────────────────────────────────────────────────────────────────────
"""
        
        # Overall statistics
        report += f"Total Actions: {system_analytics.get('total_actions', 0)}\n"
        report += f"Success Rate: {system_analytics.get('success_rate', 0)}%\n"
        report += f"Average Response Time: {system_analytics.get('average_response_time', 0)}s\n"
        
        # Component usage
        component_usage = system_analytics.get('component_usage', {})
        if component_usage:
            report += f"\n🏗️  COMPONENT USAGE:\n"
            for component, count in sorted(component_usage.items(), key=lambda x: x[1], reverse=True):
                report += f"  • {component}: {count} actions\n"
        
        # Action types
        action_types = system_analytics.get('action_types', {})
        if action_types:
            report += f"\n🎯 ACTION TYPES:\n"
            for action, count in sorted(action_types.items(), key=lambda x: x[1], reverse=True)[:5]:
                report += f"  • {action}: {count} times\n"
        
        # User activity
        user_activity = system_analytics.get('user_activity', {})
        if user_activity:
            report += f"\n👥 USER ACTIVITY:\n"
            for user, count in sorted(user_activity.items(), key=lambda x: x[1], reverse=True)[:5]:
                report += f"  • User {user}: {count} actions\n"
        
        # Most active metrics
        most_active_user = system_analytics.get('most_active_user')
        most_used_component = system_analytics.get('most_used_component')
        most_common_action = system_analytics.get('most_common_action')
        
        report += f"\n🏆 TOP METRICS:\n"
        if most_active_user:
            report += f"  • Most Active User: {most_active_user}\n"
        if most_used_component:
            report += f"  • Most Used Component: {most_used_component}\n"
        if most_common_action:
            report += f"  • Most Common Action: {most_common_action}\n"
        
        report += f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                              END OF REPORT                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        
        return report
    
    def generate_user_report(self, user_id: str, time_period: str = "month") -> str:
        """Generate a user-specific report"""
        user_analytics = self.get_user_analytics(user_id, time_period)
        
        if not user_analytics:
            return f"No data found for user {user_id} in the last {time_period}"
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           USER ANALYTICS REPORT                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

👤 USER: {user_id}
📅 PERIOD: {time_period.upper()}
────────────────────────────────────────────────────────────────────────────────
"""
        
        # User statistics
        report += f"Total Actions: {user_analytics.get('total_actions', 0)}\n"
        report += f"Success Rate: {user_analytics.get('success_rate', 0)}%\n"
        
        response_times = user_analytics.get('response_times', {})
        if response_times:
            report += f"Average Response Time: {response_times.get('average', 0)}s\n"
            report += f"Response Time Range: {response_times.get('minimum', 0)}s - {response_times.get('maximum', 0)}s\n"
        
        # Component usage
        component_usage = user_analytics.get('component_usage', {})
        if component_usage:
            report += f"\n🏗️  COMPONENT USAGE:\n"
            for component, count in sorted(component_usage.items(), key=lambda x: x[1], reverse=True):
                report += f"  • {component}: {count} actions\n"
        
        # Action types
        action_types = user_analytics.get('action_types', {})
        if action_types:
            report += f"\n🎯 ACTION TYPES:\n"
            for action, count in sorted(action_types.items(), key=lambda x: x[1], reverse=True):
                report += f"  • {action}: {count} times\n"
        
        # Most used metrics
        most_used_action = user_analytics.get('most_used_action')
        most_used_component = user_analytics.get('most_used_component')
        
        report += f"\n🏆 USER PREFERENCES:\n"
        if most_used_action:
            report += f"  • Most Used Action: {most_used_action}\n"
        if most_used_component:
            report += f"  • Most Used Component: {most_used_component}\n"
        
        report += f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                              END OF REPORT                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        
        return report
    
    def generate_component_report(self, component: str, time_period: str = "month") -> str:
        """Generate a component-specific report"""
        component_analytics = self.get_component_analytics(component, time_period)
        
        if not component_analytics:
            return f"No data found for component {component} in the last {time_period}"
        
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         COMPONENT ANALYTICS REPORT                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

🏗️  COMPONENT: {component}
📅 PERIOD: {time_period.upper()}
────────────────────────────────────────────────────────────────────────────────
"""
        
        # Component statistics
        report += f"Total Actions: {component_analytics.get('total_actions', 0)}\n"
        report += f"Success Rate: {component_analytics.get('success_rate', 0)}%\n"
        report += f"Average Response Time: {component_analytics.get('average_response_time', 0)}s\n"
        
        # Action types
        action_types = component_analytics.get('action_types', {})
        if action_types:
            report += f"\n🎯 ACTION TYPES:\n"
            for action, count in sorted(action_types.items(), key=lambda x: x[1], reverse=True):
                report += f"  • {action}: {count} times\n"
        
        # User activity
        user_activity = component_analytics.get('user_activity', {})
        if user_activity:
            report += f"\n👥 USER ACTIVITY:\n"
            for user, count in sorted(user_activity.items(), key=lambda x: x[1], reverse=True):
                report += f"  • User {user}: {count} actions\n"
        
        # Most common metrics
        most_common_action = component_analytics.get('most_common_action')
        most_active_user = component_analytics.get('most_active_user')
        
        report += f"\n🏆 COMPONENT METRICS:\n"
        if most_common_action:
            report += f"  • Most Common Action: {most_common_action}\n"
        if most_active_user:
            report += f"  • Most Active User: {most_active_user}\n"
        
        report += f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                              END OF REPORT                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        
        return report
    
    def create_visualizations(self, time_period: str = "month") -> Dict[str, str]:
        """Create visualizations for analytics data"""
        system_analytics = self.get_system_analytics(time_period)
        
        visualizations = {}
        
        # Component usage pie chart
        component_usage = system_analytics.get('component_usage', {})
        if component_usage:
            plt.figure(figsize=(10, 6))
            labels = list(component_usage.keys())
            sizes = list(component_usage.values())
            plt.pie(sizes, labels=labels, autopct='%1.1f%%')
            plt.title(f'Component Usage ({time_period})')
            plt.axis('equal')
            
            chart_path = self.data_directory / f"component_usage_{time_period}.png"
            plt.savefig(chart_path)
            plt.close()
            visualizations['component_usage'] = str(chart_path)
        
        # Hourly usage line chart
        hourly_usage = system_analytics.get('hourly_usage', {})
        if hourly_usage:
            plt.figure(figsize=(12, 6))
            hours = sorted(hourly_usage.keys())
            counts = [hourly_usage[hour] for hour in hours]
            plt.plot(hours, counts, marker='o')
            plt.title(f'Hourly Usage Pattern ({time_period})')
            plt.xlabel('Hour of Day')
            plt.ylabel('Number of Actions')
            plt.grid(True)
            
            chart_path = self.data_directory / f"hourly_usage_{time_period}.png"
            plt.savefig(chart_path)
            plt.close()
            visualizations['hourly_usage'] = str(chart_path)
        
        # Daily usage bar chart
        daily_usage = system_analytics.get('daily_usage', {})
        if daily_usage:
            plt.figure(figsize=(15, 6))
            days = sorted(daily_usage.keys())
            counts = [daily_usage[day] for day in days]
            plt.bar(range(len(days)), counts)
            plt.title(f'Daily Usage Pattern ({time_period})')
            plt.xlabel('Date')
            plt.ylabel('Number of Actions')
            plt.xticks(range(len(days)), days, rotation=45)
            plt.grid(True)
            
            chart_path = self.data_directory / f"daily_usage_{time_period}.png"
            plt.savefig(chart_path)
            plt.close()
            visualizations['daily_usage'] = str(chart_path)
        
        return visualizations
    
    def export_analytics(self, format: str = "json") -> str:
        """Export analytics data"""
        if format == "json":
            export_file = self.data_directory / f"analytics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # Convert analytics data to serializable format
            export_data = {
                "analytics": [asdict(item) for item in self.analytics_data],
                "system_analytics": self.get_system_analytics(),
                "export_timestamp": datetime.now().isoformat()
            }
            
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return str(export_file)
        
        return ""
    
    def get_performance_insights(self) -> Dict:
        """Get performance insights and recommendations"""
        system_analytics = self.get_system_analytics("month")
        
        insights = {
            "performance_metrics": {},
            "recommendations": [],
            "trends": {}
        }
        
        # Performance metrics
        success_rate = system_analytics.get('success_rate', 0)
        avg_response_time = system_analytics.get('average_response_time', 0)
        
        insights["performance_metrics"] = {
            "success_rate": success_rate,
            "average_response_time": avg_response_time,
            "total_actions": system_analytics.get('total_actions', 0)
        }
        
        # Recommendations based on performance
        if success_rate < 90:
            insights["recommendations"].append("System success rate is below optimal levels - consider reviewing error handling")
        
        if avg_response_time > 5:
            insights["recommendations"].append("Average response time is high - consider performance optimization")
        
        # Component usage insights
        component_usage = system_analytics.get('component_usage', {})
        if component_usage:
            most_used = max(component_usage.items(), key=lambda x: x[1])
            least_used = min(component_usage.items(), key=lambda x: x[1])
            
            insights["trends"]["most_used_component"] = most_used[0]
            insights["trends"]["least_used_component"] = least_used[0]
            
            if most_used[1] > least_used[1] * 5:
                insights["recommendations"].append(f"Component usage is heavily skewed - consider promoting {least_used[0]}")
        
        return insights


def main():
    """Main analytics dashboard function"""
    dashboard = AnalyticsDashboard()
    
    import argparse
    parser = argparse.ArgumentParser(description="AI Writing Companion Analytics Dashboard")
    parser.add_argument("--system-report", action="store_true", help="Generate system usage report")
    parser.add_argument("--user-report", type=str, help="Generate user-specific report")
    parser.add_argument("--component-report", type=str, help="Generate component-specific report")
    parser.add_argument("--period", type=str, default="month", choices=["day", "week", "month", "quarter", "year"], help="Time period for analysis")
    parser.add_argument("--visualize", action="store_true", help="Create visualizations")
    parser.add_argument("--export", action="store_true", help="Export analytics data")
    parser.add_argument("--insights", action="store_true", help="Get performance insights")
    
    args = parser.parse_args()
    
    if args.system_report:
        report = dashboard.generate_usage_report(args.period)
        print(report)
    
    elif args.user_report:
        report = dashboard.generate_user_report(args.user_report, args.period)
        print(report)
    
    elif args.component_report:
        report = dashboard.generate_component_report(args.component_report, args.period)
        print(report)
    
    elif args.visualize:
        visualizations = dashboard.create_visualizations(args.period)
        print(f"📊 Created {len(visualizations)} visualizations:")
        for chart_type, path in visualizations.items():
            print(f"  • {chart_type}: {path}")
    
    elif args.export:
        export_file = dashboard.export_analytics()
        if export_file:
            print(f"✅ Exported analytics to: {export_file}")
        else:
            print("❌ Export failed")
    
    elif args.insights:
        insights = dashboard.get_performance_insights()
        print(f"\n🔍 Performance Insights:")
        print(f"Success Rate: {insights['performance_metrics']['success_rate']}%")
        print(f"Average Response Time: {insights['performance_metrics']['average_response_time']}s")
        print(f"Total Actions: {insights['performance_metrics']['total_actions']}")
        
        if insights['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in insights['recommendations']:
                print(f"  • {rec}")
        
        if insights['trends']:
            print(f"\n📈 Trends:")
            for trend, value in insights['trends'].items():
                print(f"  • {trend}: {value}")
    
    else:
        # Default: show system report
        report = dashboard.generate_usage_report()
        print(report)


if __name__ == "__main__":
    main() 