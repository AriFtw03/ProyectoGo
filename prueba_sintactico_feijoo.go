package main

import "fmt"

func main() {
	// Slice literal y declaración corta
	montos := []float64{15.50, 20.00, 100.25}
	
	//Prueba de inicialización vacía de un slice
	facturas := []string{}

	// Prueba de indexación y operaciones matemáticas con precedencia
	subtotal := montos[0] + montos[1] * 2.0
	
	// Prueba del condicional if/else anidado con operadores relacionales
	if subtotal > 50.00 {
		subtotal = 50.00
	} else {
		subtotal = subtotal + 5.00
	}

	// Prueba de asignación simple
	facturas[0] = "F-001"

	// === ERRORES SINTÁCTICOS INTENCIONALES ===
	
	edades := []int{20, 21, 22 
	total :=
}