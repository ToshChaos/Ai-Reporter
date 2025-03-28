from flask import Flask, request, jsonify
import os
import sys

from call_service import call_service

app = Flask(__name__)

# Process report with operation
@app.route("/op", methods=["POST"])
def handle_op():
    # Print the full request data
    print("*** Operation Request received ***")

    if request.is_json:
        json_data = request.get_json()
        print("JSON Body:", json_data)

        call_id = json_data.get("call_id")
        if call_id is not None:
            # New call, save previous report
            if call_service.last_call_id and call_id != call_service.last_call_id:
                call_service.save_call()
                call_service.reset()

            # Handle operations
            call_service.process_operations(call_id, json_data)

            # Handle convo finish
            if json_data.get("done"):
                call_service.save_call(True)

    sys.stdout.flush()

    return jsonify({"message": "Report operation logged."})

# Process report with ticket
@app.route("/ticket", methods=["POST"])
def handle_ticket():
    # Print the full request data
    print("*** Ticket Request received ***")

    if request.is_json:
        json_data = request.get_json()
        print("JSON Body:", json_data)

        call_id = json_data.get("call_id")
        if call_id is not None:
            # New call, save previous report

            if call_service.last_call_id and call_id != call_service.last_call_id:
                call_service.save_call()
                call_service.reset()

            # Handle tickets
            call_service.process_tickets(call_id, json_data)
            
            # Handle convo finish
            if json_data.get("done"):
                call_service.save_call(True)

    sys.stdout.flush()

    return jsonify({"message": "Report ticket logged."})

# Html visualizer
@app.route("/stats", methods=["GET"])
def show_stats():
    return call_service.show_call_info()

# Reset all data
@app.route("/reset", methods=["GET", "POST"])
def reset_stats():
    call_service.reset()
    return jsonify({"message": "Data reset."})


if __name__ == "__main__":
    # Heroku provides this environment variable
    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
