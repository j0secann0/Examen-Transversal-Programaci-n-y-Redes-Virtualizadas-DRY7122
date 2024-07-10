from geopy.distance import distance
from geopy.geocoders import Nominatim

def obtener_coordenadas(ciudad):
    geolocator = Nominatim(user_agent="script_distancia_entre_ciudades")
    location = geolocator.geocode(ciudad)
    if location:
        return (location.latitude, location.longitude)
    else:
        raise ValueError(f"No se pudo encontrar la ubicación de {ciudad}")

def calcular_distancia(ciudad_origen, ciudad_destino):
    try:
        # Obtener coordenadas de origen y destino
        origen = obtener_coordenadas(ciudad_origen)
        destino = obtener_coordenadas(ciudad_destino)

        # Calcular distancia en millas y kilómetros
        dist_millas = distance(origen, destino).miles
        dist_km = distance(origen, destino).km

        return dist_millas, dist_km
    
    except Exception as e:
        return None, None

def main():
    print("Bienvenido al calculador de distancia entre ciudades de Chile y Argentina.")
    while True:
        ciudad_origen = input("Ingrese la ciudad de origen (Chile): ")
        ciudad_destino = input("Ingrese la ciudad de destino (Argentina): ")
        
        dist_millas, dist_km = calcular_distancia(ciudad_origen, ciudad_destino)

        if dist_millas is not None and dist_km is not None:
            print(f"La distancia entre {ciudad_origen} y {ciudad_destino} es:")
            print(f"{dist_millas:.2f} millas")
            print(f"{dist_km:.2f} kilómetros")
        else:
            print(f"No se pudo calcular la distancia entre {ciudad_origen} y {ciudad_destino}.")
        
        salir = input("Presione 's' para salir o cualquier otra tecla para realizar otro cálculo: ")
        if salir.lower() == 's':
            break

if __name__ == "__main__":
    main()
