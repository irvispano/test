
$.ajax({
    url: './array_of_animals.json',
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    data:"data",
    headers: {
        
        "Access-Control-Allow-Origin":"*"
    },
    success: function (data) {
        console.log(data)
        
        
        $.each(data, function (index,animal) {
                const html_collective_adjective =`<div class="row">`
                let column= `
                            <div class="col">
                           <a href="https://en.wikipedia.org${animal.animal_link}">
                            ${animal.animal.toUpperCase()}
                            </a> 
                            </div>
                            <div class="col"> 
                                ${animal.colateral_adjective.toUpperCase()}
                            </div>
                            <div class="col">
                            <img src="./tmp/${animal.animal}.jpg" height="60px" alt="">
                            </div>`
                const html_collective_adjective_end =`</div>`
                let total_parts_join_html = html_collective_adjective+column+html_collective_adjective_end;
                // parts.push(total_parts_join_html);
                $('.container').append(total_parts_join_html);
            })
            
            // let all_parts = parts.join("");
           
           
    
      
             
            
        }
    
});
