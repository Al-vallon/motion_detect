# motion_detect.py

import cv2 #type: ignore[import]
import numpy as np
import time

# Propriétés de la caméra pour optimiser la performance
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Résolution modérée
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)  # Fréquence d'images optimale

# Vérifier si la caméra est ouverte correctement
if not cap.isOpened():
    print("Erreur: Impossible d'accéder à la caméra")
    exit()

ret, frame1 = cap.read()
ret, frame2 = cap.read()

# Variables pour calculer le FPS
prev_time = time.time()
fps = 0

while cap.isOpened():
    # Calcul du FPS
    current_time = time.time()
    elapsed = current_time - prev_time
    if elapsed > 0:
        fps = 1.0 / elapsed
    prev_time = current_time
    
    # Détection de mouvement
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    
    # Ajuster le seuil à une valeur plus basse pour augmenter la sensibilité
    _, thresh = cv2.threshold(blur, 15, 255, cv2.THRESH_BINARY)
    
    # Augmenter le nombre d'itérations pour mieux connecter les zones de mouvement
    dilated = cv2.dilate(thresh, None, iterations=4)
    
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Créer une copie du frame pour l'affichage
    frame_display = frame1.copy()
    
    # Réduire le seuil de détection pour une sensibilité accrue
    motion_detected = False
    for c in contours:
        if cv2.contourArea(c) < 300:  # Seuil réduit pour détecter des mouvements plus petits
            continue
        motion_detected = True
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame_display, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Afficher des informations sur l'image
    cv2.putText(frame_display, f"FPS: {int(fps)}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    if motion_detected:
        cv2.putText(frame_display, "Mouvement detecte!", (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Afficher également la frame traitée pour voir le fonctionnement de la détection
    small_thresh = cv2.resize(dilated, (320, 240))
    frame_display[0:240, 0:320] = cv2.cvtColor(small_thresh, cv2.COLOR_GRAY2BGR)
    
    cv2.imshow("Motion Detection", frame_display)
    
    frame1 = frame2
    ret, frame2 = cap.read()
    
    # Touche Echap pour quitter
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
