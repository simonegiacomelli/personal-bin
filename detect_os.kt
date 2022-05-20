#!/usr/bin/env kscript

enum class Platform { Linux, Darwin, Windows, Undetermined }

/** mimics python platform system api
 * https://docs.python.org/3/library/platform.html#platform.system  */
fun platform(): Platform {
    val os = System.getProperty("os.name", "").lowercase()
    return if (os.indexOf("mac") >= 0 || os.indexOf("darwin") >= 0) Platform.Darwin
    else if (os.indexOf("win") >= 0) Platform.Windows
    else if (os.indexOf("nux") >= 0) Platform.Linux
    else Platform.Undetermined
}

fun main() {
    println(platform())
}