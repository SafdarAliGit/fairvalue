import frappe
import math

# Haversine formula to calculate the distance between two coordinates in meters
def haversine_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in meters
    R = 6371000

    # Convert degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Difference between the latitudes and longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in meters
    distance = R * c
    return distance

# Validate function to check if the employee's check-in location is within 10 meters
def validate(self, method):
    # Fetch the employee's registered latitude and longitude from the Employee doctype
    employee_doc = frappe.get_doc("Employee", self.employee)
    registered_latitude = employee_doc.custom_latitude
    registered_longitude = employee_doc.custom_longitude

    # Check if the registered location is set for the employee
    if not registered_latitude or not registered_longitude:
        frappe.throw("Registered location for the employee is not set. Please update the employee record.")

    # Check-in latitude and longitude (these are the current location values you want to validate)
    checkin_latitude = self.latitude  # Assuming these fields exist in the document
    checkin_longitude = self.longitude

    # Ensure the check-in location is provided
    if not checkin_latitude or not checkin_longitude:
        frappe.throw("Check-in location not provided. Please ensure both latitude and longitude are available.")

    # Calculate the distance between the check-in location and the registered location
    distance = haversine_distance(registered_latitude, registered_longitude, checkin_latitude, checkin_longitude)

    # Validate the distance (within 10 meters)
    if distance <= 10:
        frappe.msgprint(f"Check-in location is within {distance:.2f} meters of the allowed location.")
    else:
        frappe.throw(f"Check-in location is {distance:.2f} meters away from the allowed location. You cannot mark attendance.")

# This function will be called when the attendance document is validated.
# You can attach this function to the `Attendance` doctype in your hooks or as part of the custom script.

    
