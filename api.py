from flask import Flask, request, jsonify
import os
import sys
from flasgger import Swagger
from call_service import call_service
from persistence import get_history_by_device

app = Flask(__name__)
swagger = Swagger(app)  # Initialize OpenAPI documentation

@app.route("/op", methods=["POST"])
def handle_op():
    """
    Log an operation for a call.
    
    This endpoint records an operation performed during a call. 
    If the call ID changes, the previous call data is saved and reset.
    
    ---
    tags:
      - Operations
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - call_id
            - operation
          properties:
            call_id:
              type: string
              description: Unique identifier for the call session.
            operation:
              type: string
              description: The name of the operation performed.
    responses:
      200:
        description: Operation logged successfully.
    """
    if request.is_json:
        json_data = request.get_json()
        call_id = json_data.get("call_id")
        if call_id:
            call_service.check_new_call(call_id)

            call_service.process_operations(call_id, json_data)

    sys.stdout.flush()
    return jsonify({"message": "Operation logged successfully."})

@app.route("/ticket", methods=["POST"])
def handle_ticket():
    """
    Log a support ticket for a call.
    
    This endpoint records a support ticket associated with a call session.
    If the call ID changes, the previous call data is saved and reset.
    
    ---
    tags:
      - Tickets
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - call_id
            - ticket
          properties:
            call_id:
              type: string
              description: Unique identifier for the call session.
            ticket:
              type: object
              description: A dictionary containing ticket details (e.g., issue description, priority level).
    responses:
      200:
        description: Support ticket logged successfully.
    """
    if request.is_json:
        json_data = request.get_json()
        call_id = json_data.get("call_id")
        if call_id:
            call_service.check_new_call(call_id)

            call_service.process_tickets(call_id, json_data)

    sys.stdout.flush()
    return jsonify({"message": "Support ticket logged successfully."})

@app.route("/device", methods=["POST"])
def set_device():
    """
    Assign a device to a call session.
    
    This endpoint associates a device ID with an ongoing call session.
    
    ---
    tags:
      - Devices
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - call_id
            - device_id
          properties:
            call_id:
              type: string
              description: Unique identifier for the call session.
            device_id:
              type: string
              description: Unique identifier for the device involved in the call.
    responses:
      200:
        description: Device ID successfully linked to the call session.
    """
    if request.is_json:
        json_data = request.get_json()
        call_id = json_data.get("call_id")
        device_id = json_data.get("device_id")
        if call_id and device_id:
            call_service.check_new_call(call_id)
        
            call_service.set_device(call_id, device_id)
            return jsonify({"message": "Device ID linked to call session."})

    return jsonify({"error": "Invalid request"}), 400

@app.route("/history", methods=["GET"])
def get_history():
    """
    Retrieve past tickets and unfinished operations for a specific device.
    
    This endpoint fetches historical data, including:
    - All past support tickets
    - Any unfinished operations (marked as `finished: false`)
    
    ---
    tags:
      - History
    parameters:
      - name: device_id
        in: query
        type: string
        required: true
        description: The unique identifier of the device to fetch history for.
    responses:
      200:
        description: A JSON object containing the device’s historical records.
        schema:
          type: object
          properties:
            tickets:
              type: array
              items:
                type: object
              description: A list of past support tickets linked to the device.
            unfinished_operations:
              type: array
              items:
                type: object
              description: A list of operations that have not yet been marked as finished.
    """
    device_id = request.args.get("device_id")
    if not device_id:
        return jsonify({"error": "Missing device_id parameter"}), 400

    history = get_history_by_device(device_id)
    return jsonify(history)

@app.route("/stats", methods=["GET"])
def show_stats():
    """
    View real-time call statistics.
    
    This endpoint returns an HTML page with details of the most recent call session,
    including operations, tickets, and completion status.
    
    ---
    tags:
      - Statistics
    responses:
      200:
        description: An HTML page displaying call session statistics.
    """
    return call_service.show_call_info()

@app.route("/reset", methods=["GET", "POST"])
def reset_stats():
    """
    Reset all stored call data.
    
    This endpoint clears all stored call session data, including operations, tickets,
    and device assignments.
    
    ---
    tags:
      - Reset
    responses:
      200:
        description: Successfully reset all stored data.
    """
    call_service.reset()
    return jsonify({"message": "All data has been reset."})

@app.route("/end", methods=["GET", "POST"])
def finnish_call():
    """
    Save the call.
    
    This endpoint saves the current call data.
    
    ---
    tags:
      - Save
    responses:
      200:
        description: Successfully stored call data.
    """
    if call_service.save_call() is None:
      return jsonify({"message": "Call data saved."})
    else:
      return jsonify({"error": "Missing id"}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
