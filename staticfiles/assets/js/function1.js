

// const monthNames = [
//     "jan", "feb", "mar", "apr", "may", "jun",
//     "jul", "aug", "sep", "oct", "nov", "dec"
// ];

// Review
$("#commentForm").submit(function (e) {
    e.preventDefault();
    

    const date = new Date(); // Current date

    // Format the date to match "Jan. 29, 2025, 8:57 a.m."
    const formattedDate = date.toLocaleString("en-US", {
        month: "short", // "Jan"
        day: "numeric", // "29"
        year: "numeric", // "2025"
        hour: "numeric", // "8"
        minute: "2-digit", // "57"
        hour12: true // Use 12-hour format with a.m./p.m.
    }).replace("AM", "a.m.").replace("PM", "p.m."); // Ensure lowercase "a.m./p.m."


    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",
        success: function (response) {
            console.log("comment saved to db");


            if (response.bool) {
                $("#review-res").html("Review Added Successfully.")
                $(".hide-comment-form").hide()
                $(".add-review").hide()


                let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                    _html+='<div class="user justify-content-between d-flex">'
                    _html+='<div class="thumb text-center">'
                    _html+='<img src="https://imgs.search.brave.com/mDztPWayQWWrIPAy2Hm_FNfDjDVgayj73RTnUIZ15L0/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90NC5m/dGNkbi5uZXQvanBn/LzAyLzE1Lzg0LzQz/LzM2MF9GXzIxNTg0/NDMyNV90dFg5WWlJ/SXllYVI3TmU2RWFM/TGpNQW15NEd2UEM2/OS5qcGc" alt="" />'
                    _html+='<a href="#" class="font-heading text-brand">'+ response.context.user +'</a>'
                    _html+='</div>'

                    _html+='<div class="desc">'
                    _html+='<div class="d-flex justify-content-between mb-10">'
                    _html+='<div class="d-flex align-items-center">' 
                    _html+='<span class="font-xs text-muted">'+ formattedDate +' </span>'
                    _html+='</div>'
                    

                    for(let i=1 ; i<=response.context.rating ; i++){
                        _html += '<i class="fas fa-star text-warning"></i>'
                    }
                    _html+='</div>'
                    _html+='<p class="mb-10">'+ response.context.review   +' </p>'

                    _html+='</div>'
                    _html+='</div>'
                    _html+='</div>'
                    $(".comment-list").prepend(_html)
            }
            
        }
    });
});


// Filter Product By Category And Vendor
$(document).ready(function(){

    $(".filter-checkbox , #price-filter-btn ").on("click" , function(){
        console.log("A Checkbox Have been clicked");
        

        let filter_object = {};


        let min_price = $("#max_price").attr("min");
        let max_price = $("#max_price").val();

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")

            // console.log("Filter Value Is :" ,  filter_value);
            // console.log("Filter Key Is :" ,  filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter='+ filter_key +']:checked')).map(function(element){
                return element.value
            })
        })
        console.log("Filter Object is :" , filter_object);
        $.ajax({
            url: '/filter-products' ,
            data: filter_object ,
            dataType: 'json',
            beforeSend : function(){
                console.log("Trying to filter product...");
            },
            success : function(response) {
                console.log(response);
                console.log("Data filtered successfully");

                let productCount = response.product_count;
                let productText = productCount === 1 ? "item" : "items"; // Pluralization check
                

                // Update the product count and pluralized text
                $("#product-count").html(productCount);  // Update the count number
                $("#product-count-text").html(productText);  // Apply pluralization
                $("#filtered-product").html(response.data);
            }
        })
    })

    // Filter Product By Price
    $("#max_price").on("blur" , function(){
        let min_price = $(this).attr("min");
        let max_price = $(this).attr("max");
        let current_price = $(this).val();

        min_price = (min_price*100)/100
        max_price = (max_price*100)/100

        if (current_price > parseInt(max_price)){
            $(this).val(max_price);
        }
        else if (current_price < parseInt(min_price)){
            $(this).val(min_price);
        }


    })


    $(".add-to-cart-btn").on("click" , function(){
        let this_val = $(this)
        let index =this_val.attr("data-index")



        let product_price = $(".current-product-price-" + index).text();
        let product_quantity = $(".product-quantity-" + index).val();
        let product_id = $(".product-id-" + index).val();
        let product_title = $(".product-title-" + index).val();
        let product_pid = $(".product-pid-" + index).val()
        let product_image = $(".product-image-" + index).val();
        


    // console.log(`product_price : ${product_price}
    //         \n product_quantity : ${product_quantity}
    //         \n product_id : ${product_id}  
    //         \n product_title : ${product_title} 
    //         \n product-pid : ${product_pid}
    //         \n product_image : ${product_image}
            
            
    //         `);

    $.ajax({
        url : '/add-to-cart',
        data : {
            'id':product_id ,
            'qty' : product_quantity ,
            'title' : product_title ,
            'price' : product_price ,
            'image' : product_image ,
            'pid' : product_pid ,
        },
        dataType: 'json',
        beforeSend : function () { 
            console.log(`Adding product to cart ....`);
            
        } ,
        success : function(response){
            this_val.html("✓")
            console.log(`Added product to cart ....`);
            $(".cart-items-count").text(response.totalCartItems)
        }

    })

    }) 


    // Delete From Cart
    $(document).on("click", '.delete-product', function(){
        let product_id = $(this).attr("data-product");
        let this_val = $(this)

        console.log(`product_id : ${product_id}
            `);

        $.ajax({
            
            url: "/delete-from-cart",
            data: {"id":product_id},
            dataType: "json",
            beforeSend : function () { 
                this_val.hide()
                console.log(`Deleting product from cart ....`);
                
            } ,
            success: function (response) {
                this_val.show();
                $(".cart-items-count").text(response.totalCartItems);
                $("#cart-list").html(response.data)
                
            }
        });
        

    })



    
})



    // Update From Cart
    $(document).ready(function () {
        $(document).on("click", ".update-product", function () {  // ✅ Works even after AJAX updates
            let product_id = $(this).attr("data-product");
            let qtyInput = $(this).closest("tr").find(".qty-val"); // ✅ Get quantity from the same row
            let newQuantity = parseInt(qtyInput.val()) || 1; // ✅ Ensure valid quantity
            let this_val = $(this);
    
            console.log(`
                product_id : ${product_id}
                newQuantity : ${newQuantity}
            `);
    
            $.ajax({
                url: "/update-cart",
                data: {
                    "id": product_id,
                    "qty": newQuantity,
                },
                dataType: "json",
                beforeSend: function () {
                    console.log(`Updating product from cart...`);
                    this_val.attr("disabled", true); // Disable button to prevent multiple clicks
                },
                success: function (response) {
                    $(".cart-items-count").text(response.totalCartItems);
                    this_val.attr("disabled", false);
                    $("#cart-list").html(response.data);  // ✅ Re-render cart
                },
                error: function () {
                    console.log("Error updating cart.");
                    this_val.attr("disabled", false);
                }
            });
        });
    });
    
    


// Add to cart

// $("#add-to-cart-btn").on("click" , function(){
//     let product_price = $("#current-product-price").text();
//     let product_quantity = $("#product-quantity").val();
//     let product_id = $(".product-id").val();
//     let product_title = $(".product-title").val();
//     let this_val = $(this)


// console.log(`product_price : ${product_price}   \n product_quantity : ${product_quantity}  \n product_id : ${product_id}   \n product_title : ${product_title} \n this_val : ${this_val}`);

// $.ajax({
//     url : '/add-to-cart',
//     data : {
//         'id':product_id ,
//         'qty' : product_quantity ,
//         'title' : product_title ,
//         'price' : product_price 
//     },
//     dataType: 'json',
//     beforeSend : function () { 
//         console.log(`Adding product to cart ....`);
        
//     } ,
//     success : function(response){
//         this_val.html("Item Add to Cart")
//         console.log(`Added product to cart ....`);
//         $(".cart-items-count").text(response.totalCartItems)
//     }

// })

// }) 




