/*
  Archivo de prueba diseñado para validar los aportes de Diego Alfonzo.
  Debe validar correctamente:
  - Mapas asociativos
  - Operadores relacionales (==, !=, <, >, <=, >=)
  - Operadores lógicos (&&, ||, !)
  - Comentarios (de una y de múltiples líneas)
  - Delimitadores (parentesis, llaves, comas, puntos y dos puntos)
  - Literales de cadena (LITERAL_STRING) y decimales (LITERAL_FLOAT)
*/
package main

import "fmt"

func main() {
    // Declaración y asignación de un mapa asociativo (Clave string, Valor int)
    edades := map[string]int{"Diego": 21, "Arianna": 20, "Matias": 22}

    // Declaración y asignación de un mapa asociativo (Clave string, Valor float64)
    precios := map[string]float64{"manzana": 1.99, "banana": 0.85}

    // Operadores lógicos y relacionales
    x := 10.5
    y := 20.0

    if x < y && y >= 15.0 {
        fmt.Println("Cumple condicion logica")
    }

    if x == 10.5 || y != 20.0 {
        fmt.Println("Otra condicion")
    }

    noValido := !false

    // Impresión usando delimitadores
    fmt.Println(edades["Diego"], precios["manzana"], noValido)

    // Errores sencillos (caracteres no reconocidos)
    @
    $
    #

    // Errores más complejos (cadenas sin cerrar)
    cadenaIncompleta := "Esta cadena de texto nunca se cierra
    
    cadenaRawIncompleta := `Esta cadena tampoco se cierra
}

/* Comentario se queda abierto al final del archivo

