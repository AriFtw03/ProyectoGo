package main

import "fmt"

// 3. Estructuras personalizadas
type Persona struct {
    Nombre string
    Edad int
}

func main() {
    var entrada string

    // 1. Declaración en bloque
    var (
        x int = 10
        y string
    )
    
    // Impresión y Solicitud de Datos (Común)
    fmt.Println("Mensaje de prueba", x)
    fmt.Scanln(&entrada)
    
    // 2. Estructura switch
    switch x {
    case 1:
        fmt.Println("Uno")
    default:
        fmt.Println("Otro")
    }

    // 4. Funciones anónimas / closures
    operacion := func(n int) int {
        return n * 2
    }
    
    fmt.Println(operacion(x))

    // === ERRORES SINTÁCTICOS INTENCIONALES ===
    // Error 1: Estructura condicional mal formada (falta la llave de apertura)
    if x > 10 fmt.Println("Error 1")

    // Error 2: Expresión aritmética incompleta y paréntesis suelto
    resultadoErroneo := (5 + ) * 2
}
