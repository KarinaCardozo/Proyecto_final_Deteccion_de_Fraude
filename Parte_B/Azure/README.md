# 1) Docker Hub + Web App
---

## Para crear la imagen de nuestra primer versión 1.0
```
docker build -t proyecto_final_kcardozo:1.0 .
```

**-t:** tags

## Para crear el container
```
docker run -p 80:80 proyecto_final_kcardozo:1.0
```

**-p:** publish

## Para taggear la versión de la imagen
```
docker tag proyecto_final_kcardozo:1.0 karinacardozo/proyecto_final_kcardozo:1.0

```

## Para registrarse en Docker Hub
```
docker login
```

## Luego de registrarse, pushear la imagen
```
docker push karinacardozo/proyecto_final_kcardozo:1.0
```

# 2) Container Registry + Web App
---

## Para crear la imagen
```
docker build -t proyecto_final_kcardozo:1.0 .
```

**-t:** tags

## Para crear el container
```
docker run -p 80:80 -e ID_USER=Carlos123 proyecto_final_kcardozo:1.0
```

**-p:** publish

**-e:** env -> Variable de entorno

## Para taggear la versión de la imagen
```
docker tag proyecto_final_kcardozo:1.0 <NOMBRE DEL CONTAINER REGISTRY>.azurecr.io/proyecto_final_kcardozo:1.0

docker tag proyecto_final_kcardozo:1.0 travelinsurance.azurecr.io/proyecto_final_kcardozo:1.0
```

## Para registrarse en Azure
```
docker login <NOMBRE DEL CONTAINER REGISTRY>.azurecr.io

docker login travelinsurance.azurecr.io
```

## Luego de registrarse, pushear la imagen
```
docker push <NOMBRE DEL CONTAINER REGISTRY>.azurecr.io/proyecto_final_kcardozo:1.0

docker push travelinsurance.azurecr.io/proyecto_final_kcardozo:1.0
```
