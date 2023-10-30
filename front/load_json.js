
$.ajax({
    url: './collateral_adjectives_animals.json',
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    data:"data",
    success: function (data) {
        

        $.each(data, function (collateral_adjective,row) {   
           
            let parts = [];
            
            $.each(row, function (index2,column_data) {
              
                const html_collective_adjective =`<div class="row">`
                let column= `
                            <div class="col">
                            ${collateral_adjective.toUpperCase()}
                            </div>
                            <div class="col"> 
                                ${column_data[0]}
                            </div>
                            <div class="col">
                            <img src="./tmp/${column_data[0]}.jpg" height="60px" alt="">
                            </div>`
                const html_collective_adjective_end =`</div>`
                let total_parts_join_html = html_collective_adjective+column+html_collective_adjective_end;
                parts.push(total_parts_join_html);
            })
            
            let all_parts = parts.join("");
           
           
    
      
             
            $(".container").append(all_parts);
        });
    }
});
