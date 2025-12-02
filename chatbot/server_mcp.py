from mcp.server.fastmcp import FastMCP
import psycopg2, json
import asyncio
import os

# mcp = FastMCP("ToolsVitualMCP", dependencies=["psycopg2"])
mcp = FastMCP("ToolsVitualMCP", dependencies=["psycopg2-binary"])

# get_connection postgresql
def get_connection():
    """ establish a database connection """
    print("Establishing database connection...")
    url = os.getenv("DATABASE_URL")
    print(f"Database URL: {url}")
    conn = psycopg2.connect(url)
    return conn

# get_doctor
@mcp.tool()
def all_doctors():
    """ fetch all doctors from the database """

    print("Fetching all doctors from the database...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors;")
        rows = cursor.fetchall()
        results = [dict(zip([desc[0] for desc in cursor.description], row)) for row in rows]
        return json.dumps(results, indent=4, sort_keys=True, default=str)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# get_doctor_by_name
@mcp.tool()
def get_doctor_by_name(name: str) -> str:
    """ fetch doctor by name from the database """

    print("Fetching doctor by name from the database...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors WHERE name = %s;", (name,))
        rows = cursor.fetchall()
        results = [dict(zip([desc[0] for desc in cursor.description], row)) for row in rows]
        return json.dumps(results, indent=4, sort_keys=True, default=str)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# get_doctor_by_specialty
@mcp.tool()
def get_doctor_by_specialty(specialty: str) -> str:
    """ fetch doctor by specialty from the database """

    print("Fetching doctor by specialty from the database...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors WHERE specialty = %s;", (specialty,))
        rows = cursor.fetchall()
        results = [dict(zip([desc[0] for desc in cursor.description], row)) for row in rows]
        return json.dumps(results, indent=4, sort_keys=True, default=str)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# get_patient_by_name
@mcp.tool()
def get_patient_by_name(name: str) -> str:
    """ fetch all patients from the database """

    print("Fetching all patients from the database...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE name = %s;", (name,))
        rows = cursor.fetchall()
        results = [dict(zip([desc[0] for desc in cursor.description], row)) for row in rows]
        return json.dumps(results, indent=4, sort_keys=True, default=str)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# get_patient_by_cpf
@mcp.tool()
def get_patient_by_cpf(cpf: str) -> str:
    """ fetch patient by CPF from the database """

    print("Fetching patient by CPF from the database...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE cpf = %s;", (cpf,))
        rows = cursor.fetchall()
        results = [dict(zip([desc[0] for desc in cursor.description], row)) for row in rows]
        return json.dumps(results, indent=4, sort_keys=True, default=str)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"
    finally:
        cursor.close()
        conn.close()

#get_appointments_by_doctor_id
# get_appointments_by_doctor_name
@mcp.tool()
def get_appointments_by_doctor_name(doctor_name: str) -> str:
    """ fetch appointments by doctor name from the database """

    print("Fetching appointments by doctor name from the database...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.* FROM appointments a
            JOIN doctors d ON a.doctor_id = d.id
            WHERE d.name = %s;
        """, (doctor_name,))
        rows = cursor.fetchall()
        results = [dict(zip([desc[0] for desc in cursor.description], row)) for row in rows]
        return json.dumps(results, indent=4, sort_keys=True, default=str)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# get_appointments_by_patient_cpf
@mcp.tool()
def get_appointments_by_patient_cpf(patient_cpf: str) -> str:
    """ fetch appointments by patient CPF from the database """

    print("Fetching appointments by patient CPF from the database...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.* FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            WHERE p.cpf = %s;
        """, (patient_cpf,))
        rows = cursor.fetchall()
        results = [dict(zip([desc[0] for desc in cursor.description], row)) for row in rows]
        return json.dumps(results, indent=4, sort_keys=True, default=str)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# get_appointments_by_patient_name
@mcp.tool()
def get_appointments_by_patient_name(patient_name: str) -> str:
    """ fetch appointments by patient name from the database """

    print("Fetching appointments by patient name from the database...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.* FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            WHERE p.name = %s;
        """, (patient_name,))
        rows = cursor.fetchall()
        results = [dict(zip([desc[0] for desc in cursor.description], row)) for row in rows]
        return json.dumps(results, indent=4, sort_keys=True, default=str)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# add_patient
@mcp.tool()
def add_patient(
        name: str, cpf: str, phone: str, birthdate: str = None, address: str = None, has_partner: bool = False) -> str:
    """ add a new patient to the database """

    print("Adding a new patient to the database...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO patients (name, cpf, phone, birthdate, address, has_partner, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
            RETURNING id;
        """, (name, cpf, phone, birthdate, address, has_partner))
        patient_id = cursor.fetchone()[0]
        conn.commit()
        return f"Patient added with ID: {patient_id}"
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# add_appointment
@mcp.tool()
def add_appointment(
        doctor_id: int, patient_id: int, datetime: str, status: str = "SCHEDULED", reason: str = None,
        prescription: str = None, notes: str = None) -> str:
    """ add a new appointment to the database """
    print("Adding a new appointment to the database...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO appointments (doctor_id, patient_id, datetime, status, reason, prescription, notes, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            RETURNING id;
        """, (doctor_id, patient_id, datetime, status, reason, prescription, notes))
        appointment_id = cursor.fetchone()[0]
        conn.commit()
        return f"Appointment added with ID: {appointment_id}"
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return f"An error occurred: {str(e)}"
    finally:
        cursor.close()
        conn.close()

# # Example usage (uncomment to test)
# async def main():
#     # doctors = all_doctors()
#     # print("Doctors:", doctors)
#     # doctors = get_doctor_by_name("Dr. Carlos Oliveira")
#     # print("Doctors:", doctors)
#     # doctors = get_doctor_by_specialty("Cardiologia")
#     # print("Doctors:", doctors)
#     # patient = get_patient_by_name("Alice Pereira")
#     # print("Patient:", patient)
#     # patient = get_patient_by_cpf("11122233344")
#     # print("Patient:", patient)
#     # appointments = get_appointments_by_doctor_name("Dr. Carlos Oliveira")
#     # print("Appointments:", appointments)
#     # appointments = get_appointments_by_patient_cpf("11122233344")
#     # print("Appointments:", appointments)
#     # appointments = get_appointments_by_patient_name("Alice Pereira")
#     # print("Appointments:", appointments)
#     # add_patient_response = add_patient(
#     #     name="João Silva",
#     #     cpf="15566677788",
#     #     phone="51987654321"
#     # )
#     # print("Add Patient Response:", add_patient_response)
#     add_appointment_response = add_appointment(
#         doctor_id=1,
#         patient_id=1,
#         datetime="2025-12-15 14:30:00",
#         reason="Consulta de rotina"
#     )
#     print("Add Appointment Response:", add_appointment_response)

# if __name__ == "__main__":
#     asyncio.run(main())

 # execute and return the stdio output
if __name__ == "__main__":
    mcp.run(transport="stdio")