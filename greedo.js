function greedo_accumulate(data, date_col, col_col, val_col, filter_cols, filter_val)
{
	var accum = {};
	var cols = {};

	for (var x = 0; x < data.length; x++) {
		var row = data[x];

		var date = row[date_col];
		var col = row[col_col];
		var val = row[val_col];

		if (!accum[date]) accum[date] = {};

		if (val < filter_val) {
			val = 0;
		} else if (!filter_cols[col]) cols[col] = true;

		accum[date][col] = val;
	}

	return {
		'accum': accum,
		'cols': Object.keys(cols)
	};
}

function greedo_flatten(accum, cols)
{
	var flattened = [];

	var accum_keys = Object.keys(accum);

	for (var x = 0; x < accum_keys.length; x++) {
		var row = [];

		var k = accum_keys[x];
		var v = accum[k];

		row.push(k);

		for (var y = 0; y < cols.length; y++) {
			var colv = v[cols[y]];
			if (!colv) colv = 0;
			row.push(colv);
		}

		flattened.push(row);
	}

	return flattened;
}

function google_draw_line(data, cols, element_id, title, width, height)
{
	google.charts.load('current', {'packages':['line']});
	google.charts.setOnLoadCallback(function () {

		var datat = new google.visualization.DataTable();

		datat.addColumn('string', 'Day');

		for (var x = 0; x < cols.length; x++)
			datat.addColumn('number', cols[x]);

		datat.addRows(data);

		var formatter = new google.visualization.NumberFormat({pattern:'0.00'});
		for (var x = 0; x < cols.length; x++)
			formatter.format(datat, x + 1);

		formatter = new google.visualization.DateFormat({pattern:'YYYY-MM-DD'});
		formatter.format(datat, 0);

		var chart = new google.charts.Line(document.getElementById(element_id));
		chart.draw(datat, google.charts.Line.convertOptions({
			chart: {
				title: title,
			},
			width: width,
			height: height
		}));
	});
}

function google_draw_stacked(data, cols, element_id, title, width, height)
{
	google.charts.load('current', {'packages':['bar']});
	google.charts.setOnLoadCallback(function () {

		var datat = new google.visualization.DataTable();

		datat.addColumn('string', 'Day');

		for (var x = 0; x < cols.length; x++)
			datat.addColumn('number', cols[x]);

		datat.addRows(data);

		var formatter = new google.visualization.NumberFormat({pattern:'0.00'});
		for (var x = 0; x < cols.length; x++)
			formatter.format(datat, x + 1);

		formatter = new google.visualization.DateFormat({pattern:'YYYY-MM-DD'});
		formatter.format(datat, 0);

		var chart = new google.charts.Bar(document.getElementById(element_id));
		chart.draw(datat, google.charts.Bar.convertOptions({
			chart: {
				title: title,
			},
			width: width,
			height: height,
			isStacked: 'relative'
		}));
	});
}
