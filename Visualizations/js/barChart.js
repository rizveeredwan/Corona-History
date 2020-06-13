
function createBarChart(id,key_list,data_list,x_label, y_label,x_axis_categories){
  let columns_info=[];
  let temp=[];
  for(let i=0;i<key_list.length;i++){
    temp=[];
    temp.push(key_list[i]);
    for(let j=0;j<data_list[i].length;j++){
      temp.push(data_list[i][j]);
    }
    columns_info.push(temp);
  }

  var chart = c3.generate({
        bindto: '#'+id,
        data: {
          columns: columns_info,
          type: 'bar'
        },
        axis: {
          x: {
            label: {
              text: x_label,
              position: 'outer-center',
            },
            type: 'category',
            categories: x_axis_categories,
            tick: {
              centered: true
            }
          },
          y: {
            label: {
              text: y_label,
              position: 'outer-middle'
            },
            //max: 10,
            //min: 0,
            padding: {
              top: 0,
              bottom: 0
            }
          }
        },
        legend: {
          show: true
        }
      });

    /*var chart = c3.generate({
      bindto: '#'_id,
      data: {
          columns: columns_info,
          type: 'bar'
      },
      axis: {
          x: {
            label: {
              text: x_label,
              position: 'outer-center',
            },
            type: 'category',
            categories: x_axis_categories,
            tick: {
              centered: true
            }
          },
          y: {
            label: {
              text: y_label,
              position: 'outer-middle'
            },
            max: 10,
            min: 0,
            padding: {
              top: 0,
              bottom: 0
            }
          }
        },
        legend: {
          show: false
      },
      bar: {
          width: {
              ratio: 0.5 // this makes bar width 50% of length between ticks
          }
          // or
          //width: 100 // this makes bar width 100px
      }
  }); */
}
