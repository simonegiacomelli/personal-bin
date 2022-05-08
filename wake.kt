#!/usr/bin/env kscript

import java.util.Properties

//INCLUDE common.kt

fun main(args: Array<String>) {
    val host = args.firstOrNull()
    if (host == null) {
        println("Please, specify host name to wake")
        return
    }
    val file = folderOfScript().resolve("personal-bin-config/wakeonlan.properties").canonicalFile
    val p = Properties().apply { load(file.reader()) }
    val key = "host.$host"
    val mac = p.getOrDefault(key, null) ?: return println("Configuration key `$key` not found in `$file`")

    "wakeonlan $mac".runCommandInheritIO()
}


