report_template = '''
<!DOCTYPE html>
<html>
<head>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 40px;
    }}

    h1 {{
      color: #333;
      font-size: 24px;
      margin-bottom: 10px;
    }}

    h2 {{
      color: #555;
      font-size: 20px;
      margin-bottom: 10px;
    }}

    ul {{
      list-style-type: decimal;
      padding-left: 20px;
      margin-top: 0;
    }}
    
    .summ_points {{
      list-style-type: disc;
      padding-left: 20px;
      margin-top: 0;
    }}

    ul li {{
      margin-bottom: 5px;
    }}

    .class-link {{
      color: #007bff;
      text-decoration: none;
    }}

    .class-link:hover {{
      text-decoration: underline;
    }}

    .summary {{
      color: #888;
    }}

    .summary:before {{
      font-family: "Font Awesome 5 Free";
      font-weight: 900;
      margin-right: 5px;
    }}
  </style>
</head>
<body>
  <h1>{module_name}</h1>
  <h2>{batch_name}</h2>

  <ul id="class-list"></ul>

  <script>
    function fillClassList(classData) {{
      var classList = document.getElementById("class-list");

      classData.forEach(function(classItem, index) {{
        var li = document.createElement("li");
        var className = document.createElement("h3");
        var link = document.createElement("a");
        var class_summary = document.createElement("p");

        link.href = classItem.meeting_link;
        link.className = "class-link";
        link.textContent = classItem.class_title;
        class_summary.innerHTML = "<strong>Summary: </strong>" + classItem.summary + "<br><br>" +
                "If anyone was not able to attend the lecture live, please do watch the recording before the next lecture or as early as possible as we covered a lot of important topics today. Each lecture is important and would surely add to your python knowledge and aid you on your path to becoming 1% better every day.<br> Happy Learning :)";

        className.appendChild(link);

        li.appendChild(className);
        li.appendChild(class_summary);

        classList.appendChild(li);
      }});
    }}

    // Pass your data array here
    var data = {class_data};

    fillClassList(data);
  </script>
</body>
</html>

'''
