import streamlit as st

st.set_page_config(page_title="Transmission vs Congestion Delay Analyzer", layout="centered")

st.title("📡 Transmission vs Congestion Delay Analyzer - Module 1")
st.subheader("🔧 Input Parameters")

# User Inputs
packet_size = st.slider("📦 Packet Size (Bytes)", min_value=64, max_value=1500, value=512)
bandwidth = st.slider("📶 Bandwidth (Mbps)", min_value=1, max_value=1000, value=100)
num_packets = st.number_input("🔁 Number of Packets", min_value=1, max_value=100000, value=1000)

arrival_rate = st.slider("📥 Arrival Rate (packets/sec)", min_value=1, max_value=1000, value=200)
service_rate = st.slider("📤 Service Rate (packets/sec)", min_value=1, max_value=2000, value=500)

delay_type = st.radio("📊 Select Delay Type to Analyze", ["Transmission Delay", "Congestion Delay", "Both"])

# Button to confirm and print inputs
if st.button("✅ Submit Parameters"):
    st.success("✅ Parameters Recorded")
    st.write(f"Packet Size: **{packet_size} Bytes**")
    st.write(f"Bandwidth: **{bandwidth} Mbps**")
    st.write(f"Number of Packets: **{num_packets}**")
    st.write(f"Arrival Rate: **{arrival_rate} packets/sec**")
    st.write(f"Service Rate: **{service_rate} packets/sec**")
    st.write(f"Selected Analysis: **{delay_type}**")

    # You can store this input to a file or send to Module 2 for calculations
    user_inputs = {
        "packet_size": packet_size,
        "bandwidth": bandwidth,
        "num_packets": num_packets,
        "arrival_rate": arrival_rate,
        "service_rate": service_rate,
        "delay_type": delay_type
    }
    
    #module 2
    # Delay Calculation Engine

def transmission_delay(packet_size_bits, bandwidth_bps):
    """
    Transmission Delay = Packet Size / Bandwidth
    """
    try:
        delay = packet_size_bits / bandwidth_bps
        return round(delay, 6)
    except ZeroDivisionError:
        return float('inf')

def propagation_delay(distance_km, propagation_speed_kmps):
    """
    Propagation Delay = Distance / Propagation Speed
    """
    try:
        delay = distance_km / propagation_speed_kmps
        return round(delay, 6)
    except ZeroDivisionError:
        return float('inf')

def congestion_delay(queue_length, avg_packet_arrival_rate, avg_packet_service_rate):
    """
    Congestion Delay = Queue Length / (Service Rate - Arrival Rate)
    """
    try:
        if avg_packet_service_rate <= avg_packet_arrival_rate:
            return float('inf')  # Indicates infinite delay (congestion collapse)
        delay = queue_length / (avg_packet_service_rate - avg_packet_arrival_rate)
        return round(delay, 6)
    except ZeroDivisionError:
        return float('inf')

def total_network_delay(packet_size_bits, bandwidth_bps, distance_km, propagation_speed_kmps,
                        queue_length, arrival_rate, service_rate):
    t_delay = transmission_delay(packet_size_bits, bandwidth_bps)
    p_delay = propagation_delay(distance_km, propagation_speed_kmps)
    c_delay = congestion_delay(queue_length, arrival_rate, service_rate)
    total = t_delay + p_delay + c_delay
    return {
        "Transmission Delay (sec)": t_delay,
        "Propagation Delay (sec)": p_delay,
        "Congestion Delay (sec)": c_delay,
        "Total Delay (sec)": round(total, 6)
    }

# 🔧 Example usage
if __name__ == "__main__":
    # Sample Inputs
    packet_size = 8000            # in bits (1000 bytes)
    bandwidth = 1_000_000         # in bits per second (1 Mbps)
    distance = 1000               # in kilometers
    propagation_speed = 200_000   # in km/sec (typical fiber)
    queue_len = 10                # packets in queue
    arrival_rate = 5              # packets/sec
    service_rate = 10             # packets/sec

    delay_report = total_network_delay(packet_size, bandwidth, distance,
                                       propagation_speed, queue_len,
                                       arrival_rate, service_rate)

    print("Delay Report:")
    for k, v in delay_report.items():
        print(f"{k}: {v} sec")

