# Queue System Developer Guide

## Overview
The queue system provides standardized inter-system communication with automatic monitoring and error handling. It's designed to be simple to use while providing powerful debugging and performance monitoring capabilities.

## Quick Start

### Adding Queue Processing to a New System

```python
from queue_manager import QueueProcessor

class MyNewSystem(QueueProcessor):
    def __init__(self):
        # Always call super().__init__ with your system name
        super().__init__("my_new_system")
        
        # Your system initialization here
        self.my_data = {}
    
    def _process_item(self, item):
        """Override this method to handle your specific data types"""
        try:
            if item.data.get("type") == "my_data_type":
                # Process your data
                result = self.process_my_data(item.data)
                
                # Send result to another system if needed
                self.send_to_system("target_system", {"result": result})
            else:
                # Pass unknown items to base class
                super()._process_item(item)
                
        except Exception as e:
            # Errors are automatically logged and sent to error queue
            raise e
    
    def process_my_data(self, data):
        """Your system's specific processing logic"""
        return {"processed": data}
```

### Basic Usage Patterns

```python
# 1. Send data to another system
item_id = self.send_to_system("target_system", {"data": "value"})

# 2. Get system statistics
stats = self.get_system_stats()
print(f"Input queue size: {stats['input_queue_size']}")

# 3. Start/stop processing
self.start_processing()  # Starts background processing thread
self.stop_processing()   # Stops background processing thread
```

## Best Practices

### 1. System Naming
- Use descriptive, lowercase names: `"character_embodiment_engine"`
- Avoid spaces or special characters
- Keep names consistent across your codebase

### 2. Error Handling
- Always wrap your processing logic in try-except blocks
- Let the base class handle unknown item types
- Use specific error messages for debugging

```python
def _process_item(self, item):
    try:
        if item.data.get("type") == "my_type":
            # Your processing logic
            pass
        else:
            # Pass to base class for unknown types
            super()._process_item(item)
    except Exception as e:
        logger.error(f"Error processing item {item.id}: {e}")
        raise  # Re-raise to let base class handle it
```

### 3. Data Structure
- Use consistent data structures for your items
- Include a "type" field to identify your data
- Keep data lightweight to avoid memory issues

```python
# Good data structure
data = {
    "type": "character_update",
    "character_id": "123",
    "changes": {"personality": "updated"},
    "timestamp": time.time()
}

# Bad data structure (too heavy)
data = {
    "type": "character_update",
    "full_character_data": very_large_object,  # Don't do this
    "entire_conversation_history": huge_list   # Don't do this
}
```

### 4. Monitoring
- Check your system stats regularly
- Monitor queue sizes to prevent bottlenecks
- Set up alert callbacks for critical issues

```python
# Register alert callbacks
def my_warning_callback(alert_data):
    print(f"Warning: {alert_data['message']}")

queue_manager.register_alert_callback("warning", my_warning_callback)
```

## Common Patterns

### 1. Request-Response Pattern
```python
# System A sends request to System B
request_id = self.send_to_system("system_b", {
    "type": "request",
    "action": "process_data",
    "data": my_data
})

# System B processes and responds
def _process_item(self, item):
    if item.data.get("type") == "request":
        result = self.process_request(item.data)
        self.send_to_system("system_a", {
            "type": "response",
            "request_id": item.id,
            "result": result
        })
```

### 2. Pipeline Pattern
```python
# Data flows through multiple systems
def _process_item(self, item):
    if item.data.get("type") == "pipeline_data":
        # Process the data
        processed_data = self.process_data(item.data)
        
        # Send to next system in pipeline
        self.send_to_system("next_system", {
            "type": "pipeline_data",
            "data": processed_data,
            "stage": "completed"
        })
```

### 3. Broadcast Pattern
```python
# Send to multiple systems
def broadcast_update(self, update_data):
    systems = ["system_a", "system_b", "system_c"]
    for system in systems:
        self.send_to_system(system, {
            "type": "broadcast_update",
            "data": update_data
        })
```

## Debugging

### 1. Check System Health
```python
# Get all system statistics
global_stats = queue_manager.get_global_stats()
for system_name, stats in global_stats["system_health"].items():
    print(f"{system_name}: {stats}")
```

### 2. Monitor Bottlenecks
```python
# Check for bottlenecks
bottlenecks = queue_manager.get_global_stats()["bottlenecks"]
for bottleneck in bottlenecks:
    print(f"Bottleneck: {bottleneck}")
```

### 3. Clear Queues for Testing
```python
# Clear all queues (use carefully!)
queue_manager.reset_all_queues()

# Clear specific system
queue_manager.clear_system_queues("my_system")
```

## Performance Tips

1. **Keep Queue Sizes Small**: Monitor and clear queues regularly
2. **Use Appropriate Priorities**: Higher priority (1-10) for important items
3. **Avoid Large Data**: Don't send large objects through queues
4. **Monitor Memory**: Check queue sizes to prevent memory issues
5. **Use Timeouts**: Set appropriate timeouts for queue operations

## Troubleshooting

### Common Issues

1. **System Not Processing Items**
   - Check if `start_processing()` was called
   - Verify system is registered with queue manager
   - Check for exceptions in processing loop

2. **High Queue Sizes**
   - Check if processing is working correctly
   - Look for infinite loops or blocking operations
   - Consider increasing processing capacity

3. **Memory Issues**
   - Monitor queue sizes
   - Clear old items from queues
   - Check for memory leaks in processing logic

### Debug Commands
```python
# Check if system is registered
print("framework_cli" in queue_manager.systems)

# Check queue sizes
stats = queue_manager.get_system_stats("my_system")
print(f"Input: {stats['input_queue_size']}, Output: {stats['output_queue_size']}")

# Start monitoring
queue_manager.start_monitoring()
```

## Integration with Existing Systems

The queue system is designed to be non-intrusive. You can:

1. **Gradually migrate** existing systems to use queues
2. **Keep existing APIs** while adding queue functionality
3. **Use queues for new features** while maintaining old patterns
4. **Add monitoring** to existing systems without changing their core logic

This approach ensures you can adopt the queue system incrementally without disrupting existing functionality. 