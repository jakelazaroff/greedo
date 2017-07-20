SELECT dt, code, value FROM example WHERE dt > SUBDATE(CURDATE(), {{days}})
