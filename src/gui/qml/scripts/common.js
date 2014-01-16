var titlebarHeight = 30

function findParent(obj) {
	var objParent = obj.parent
	while (objParent != undefined) {
		print( objParent)
		objParent = objParent.parent
	}
	return objParent
}
